%pip install --upgrade openai pydantic python-dotenv rich persist-cache -qqq
%load_ext dotenv
%dotenv

# Place your API key in a file called .env
# OPENAI_API_KEY=sk-...

from pydantic import BaseModel


class Location(BaseModel):
    city: str | None
    state: str | None
    zipcode: str | None


class LineItem(BaseModel):
    description: str | None
    product_code: str | None
    category: str | None
    item_price: str | None
    sale_price: str | None
    quantity: str | None
    total: str | None


class ReceiptDetails(BaseModel):
    merchant: str | None
    location: Location
    time: str | None
    items: list[LineItem]
    subtotal: str | None
    tax: str | None
    total: str | None
    handwritten_notes: list[str]

BASIC_PROMPT = """
Given an image of a retail receipt, extract all relevant information and format it as a structured response.

# Task Description

Carefully examine the receipt image and identify the following key information:

1. Merchant name and any relevant store identification
2. Location information (city, state, ZIP code)
3. Date and time of purchase
4. All purchased items with their:
   * Item description/name
   * Item code/SKU (if present)
   * Category (infer from context if not explicit)
   * Regular price per item (if available)
   * Sale price per item (if discounted)
   * Quantity purchased
   * Total price for the line item
5. Financial summary:
   * Subtotal before tax
   * Tax amount
   * Final total
6. Any handwritten notes or annotations on the receipt (list each separately)

## Important Guidelines

* If information is unclear or missing, return null for that field
* Format dates as ISO format (YYYY-MM-DDTHH:MM:SS)
* Format all monetary values as decimal numbers
* Distinguish between printed text and handwritten notes
* Be precise with amounts and totals
* For ambiguous items, use your best judgment based on context

Your response should be structured and complete, capturing all available information
from the receipt.
"""

import base64
import mimetypes
from pathlib import Path

from openai import AsyncOpenAI

client = AsyncOpenAI()


async def extract_receipt_details(
    image_path: str, model: str = "o4-mini"
) -> ReceiptDetails:
    """Extract structured details from a receipt image."""
    # Determine image type for data URI.
    mime_type, _ = mimetypes.guess_type(image_path)

    # Read and base64 encode the image.
    b64_image = base64.b64encode(Path(image_path).read_bytes()).decode("utf-8")
    image_data_url = f"data:{mime_type};base64,{b64_image}"

    response = await client.responses.parse(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": BASIC_PROMPT},
                    {"type": "input_image", "image_url": image_data_url},
                ],
            }
        ],
        text_format=ReceiptDetails,
    )

    return response.output_parsed

from rich import print

receipt_image_dir = Path("data/test")
ground_truth_dir = Path("data/ground_truth")

example_receipt = Path(
    "data/train/Supplies_20240322_220858_Raven_Scan_3_jpeg.rf.50852940734939c8838819d7795e1756.jpg"
)
result = await extract_receipt_details(example_receipt)

walmart_receipt = ReceiptDetails(
    merchant="Walmart",
    location=Location(city="Vista", state="CA", zipcode="92083"),
    time="2023-06-30T16:40:45",
    items=[
        LineItem(
            description="SPRAY 90",
            product_code="001920056201",
            category=None,
            item_price=None,
            sale_price=None,
            quantity="2",
            total="28.28",
        ),
        LineItem(
            description="LINT ROLLER 70",
            product_code="007098200355",
            category=None,
            item_price=None,
            sale_price=None,
            quantity="1",
            total="6.67",
        ),
        LineItem(
            description="SCRUBBER",
            product_code="003444193232",
            category=None,
            item_price=None,
            sale_price=None,
            quantity="2",
            total="12.70",
        ),
        LineItem(
            description="FLOUR SACK 10",
            product_code="003444194263",
            category=None,
            item_price=None,
            sale_price=None,
            quantity="1",
            total="0.77",
        ),
    ],
    subtotal="50.77",
    tax="4.19",
    total="54.96",
    handwritten_notes=[],
)

from pydantic import BaseModel, Field

audit_prompt = """
Evaluate this receipt data to determine if it need to be audited based on the following
criteria:

1. NOT_TRAVEL_RELATED:
   - IMPORTANT: For this criterion, travel-related expenses include but are not limited
   to: gas, hotel, airfare, or car rental.
   - If the receipt IS for a travel-related expense, set this to FALSE.
   - If the receipt is NOT for a travel-related expense (like office supplies), set this
   to TRUE.
   - In other words, if the receipt shows FUEL/GAS, this would be FALSE because gas IS
   travel-related.

2. AMOUNT_OVER_LIMIT: The total amount exceeds $50

3. MATH_ERROR: The math for computing the total doesn't add up (line items don't sum to
   total)

4. HANDWRITTEN_X: There is an "X" in the handwritten notes

For each criterion, determine if it is violated (true) or not (false). Provide your
reasoning for each decision, and make a final determination on whether the receipt needs
auditing. A receipt needs auditing if ANY of the criteria are violated.

Return a structured response with your evaluation.
"""


class AuditDecision(BaseModel):
    not_travel_related: bool = Field(
        description="True if the receipt is not travel-related"
    )
    amount_over_limit: bool = Field(description="True if the total amount exceeds $50")
    math_error: bool = Field(description="True if there are math errors in the receipt")
    handwritten_x: bool = Field(
        description="True if there is an 'X' in the handwritten notes"
    )
    reasoning: str = Field(description="Explanation for the audit decision")
    needs_audit: bool = Field(
        description="Final determination if receipt needs auditing"
    )


async def evaluate_receipt_for_audit(
    receipt_details: ReceiptDetails, model: str = "o4-mini"
) -> AuditDecision:
    """Determine if a receipt needs to be audited based on defined criteria."""
    # Convert receipt details to JSON for the prompt
    receipt_json = receipt_details.model_dump_json(indent=2)

    response = await client.responses.parse(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": audit_prompt},
                    {"type": "input_text", "text": f"Receipt details:\n{receipt_json}"},
                ],
            }
        ],
        text_format=AuditDecision,
    )

    return response.output_parsed

audit_decision = await evaluate_receipt_for_audit(result)
print(audit_decision)

audit_decision = AuditDecision(
    not_travel_related=True,
    amount_over_limit=True,
    math_error=False,
    handwritten_x=False,
    reasoning="""
    The receipt from Walmart is for office supplies, which are not travel-related, thus NOT_TRAVEL_RELATED is TRUE.
    The total amount of the receipt is $54.96, which exceeds the limit of $50, making AMOUNT_OVER_LIMIT TRUE.
    The subtotal ($50.77) plus tax ($4.19) correctly sums to the total ($54.96), so there is no MATH_ERROR.
    There are no handwritten notes, so HANDWRITTEN_X is FALSE.
    Since two criteria (amount over limit and travel-related) are violated, the receipt
    needs auditing.
    """,
    needs_audit=True,
)

example_graders = [
    {
        "name": "Total Amount Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_receipt_details.total }}",
        "reference": "{{ item.correct_receipt_details.total }}",
    },
    {
        "name": "Merchant Name Accuracy",
        "type": "text_similarity",
        "input": "{{ item.predicted_receipt_details.merchant }}",
        "reference": "{{ item.correct_receipt_details.merchant }}",
        "pass_threshold": 0.8,
        "evaluation_metric": "bleu",
    },
]

# A model grader needs a prompt to instruct it in what it should be scoring.
missed_items_grader_prompt = """
Your task is to evaluate the correctness of a receipt extraction model.

The following items are the actual (correct) line items from a specific receipt.

{{ item.correct_receipt_details.items }}

The following items are the line items extracted by the model.

{{ item.predicted_receipt_details.items }}

Score 0 if the sample evaluation missed any items from the receipt; otherwise score 1.

The line items are permitted to have small differences or extraction mistakes, but each
item from the actual receipt must be present in some form in the model's output. Only
evaluate whether there are MISSED items; ignore other mistakes or extra items.
"""

example_graders.append(
    {
        "name": "Missed Line Items",
        "type": "score_model",
        "model": "o4-mini",
        "input": [{"role": "system", "content": missed_items_grader_prompt}],
        "range": [0, 1],
        "pass_threshold": 1,
    }
)

import asyncio


class EvaluationRecord(BaseModel):
    """Holds both the correct (ground truth) and predicted audit decisions."""

    receipt_image_path: str
    correct_receipt_details: ReceiptDetails
    predicted_receipt_details: ReceiptDetails
    correct_audit_decision: AuditDecision
    predicted_audit_decision: AuditDecision


async def create_evaluation_record(image_path: Path, model: str) -> EvaluationRecord:
    """Create a ground truth record for a receipt image."""
    extraction_path = ground_truth_dir / "extraction" / f"{image_path.stem}.json"
    correct_details = ReceiptDetails.model_validate_json(extraction_path.read_text())
    predicted_details = await extract_receipt_details(image_path, model)

    audit_path = ground_truth_dir / "audit_results" / f"{image_path.stem}.json"
    correct_audit = AuditDecision.model_validate_json(audit_path.read_text())
    predicted_audit = await evaluate_receipt_for_audit(predicted_details, model)

    return EvaluationRecord(
        receipt_image_path=image_path.name,
        correct_receipt_details=correct_details,
        predicted_receipt_details=predicted_details,
        correct_audit_decision=correct_audit,
        predicted_audit_decision=predicted_audit,
    )


async def create_dataset_content(
    receipt_image_dir: Path, model: str = "o4-mini"
) -> list[dict]:
    # Assemble paired samples of ground truth data and predicted results. You could
    # instead upload this data as a file and pass a file id when you run the eval.
    tasks = [
        create_evaluation_record(image_path, model)
        for image_path in receipt_image_dir.glob("*.jpg")
    ]
    return [{"item": record.model_dump()} for record in await asyncio.gather(*tasks)]


file_content = await create_dataset_content(receipt_image_dir)

from persist_cache import cache


# We're caching the output so that if we re-run this cell we don't create a new eval.
@cache
async def create_eval(name: str, graders: list[dict]):
    eval_cfg = await client.evals.create(
        name=name,
        data_source_config={
            "type": "custom",
            "item_schema": EvaluationRecord.model_json_schema(),
            "include_sample_schema": False,  # Don't generate new completions.
        },
        testing_criteria=graders,
    )
    print(f"Created new eval: {eval_cfg.id}")
    return eval_cfg


initial_eval = await create_eval(
    "Initial Receipt Processing Evaluation", example_graders
)

# Run the eval.
eval_run = await client.evals.runs.create(
    name="initial-receipt-processing-run",
    eval_id=initial_eval.id,
    data_source={
        "type": "jsonl",
        "source": {"type": "file_content", "content": file_content},
    },
)
print(f"Evaluation run created: {eval_run.id}")
print(f"View results at: {eval_run.report_url}")

def calculate_costs(fp_rate: float, fn_rate: float, per_receipt_cost: float):
    audit_cost = 2
    missed_audit_cost = 30
    receipt_count = 1e6
    audit_fraction = 0.05

    needs_audit_count = receipt_count * audit_fraction
    no_needs_audit_count = receipt_count - needs_audit_count

    missed_audits = needs_audit_count * fn_rate
    total_audits = needs_audit_count * (1 - fn_rate) + no_needs_audit_count * fp_rate

    audit_cost = total_audits * audit_cost
    missed_audit_cost = missed_audits * missed_audit_cost
    processing_cost = receipt_count * per_receipt_cost

    return audit_cost + missed_audit_cost + processing_cost


perfect_system_cost = calculate_costs(0, 0, 0)
current_system_cost = calculate_costs(0.02, 0.03, 0.20)

print(f"Current system cost: ${current_system_cost:,.0f}")

simple_extraction_graders = [
    {
        "name": "Merchant Name Accuracy",
        "type": "text_similarity",
        "input": "{{ item.predicted_receipt_details.merchant }}",
        "reference": "{{ item.correct_receipt_details.merchant }}",
        "pass_threshold": 0.8,
        "evaluation_metric": "bleu",
    },
    {
        "name": "Location City Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_receipt_details.location.city }}",
        "reference": "{{ item.correct_receipt_details.location.city }}",
    },
    {
        "name": "Location State Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_receipt_details.location.state }}",
        "reference": "{{ item.correct_receipt_details.location.state }}",
    },
    {
        "name": "Location Zipcode Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_receipt_details.location.zipcode }}",
        "reference": "{{ item.correct_receipt_details.location.zipcode }}",
    },
    {
        "name": "Time Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_receipt_details.time }}",
        "reference": "{{ item.correct_receipt_details.time }}",
    },
    {
        "name": "Subtotal Amount Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_receipt_details.subtotal }}",
        "reference": "{{ item.correct_receipt_details.subtotal }}",
    },
    {
        "name": "Tax Amount Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_receipt_details.tax }}",
        "reference": "{{ item.correct_receipt_details.tax }}",
    },
    {
        "name": "Total Amount Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_receipt_details.total }}",
        "reference": "{{ item.correct_receipt_details.total }}",
    },
    {
        "name": "Handwritten Notes Accuracy",
        "type": "text_similarity",
        "input": "{{ item.predicted_receipt_details.handwritten_notes }}",
        "reference": "{{ item.correct_receipt_details.handwritten_notes }}",
        "pass_threshold": 0.8,
        "evaluation_metric": "fuzzy_match",
    },
]

item_extraction_base = """
Your task is to evaluate the correctness of a receipt extraction model.

The following items are the actual (correct) line items from a specific receipt.

{{ item.correct_receipt_details.items }}

The following items are the line items extracted by the model.

{{ item.predicted_receipt_details.items }}
"""

missed_items_instructions = """
Score 0 if the sample evaluation missed any items from the receipt; otherwise score 1.

The line items are permitted to have small differences or extraction mistakes, but each
item from the actual receipt must be present in some form in the model's output. Only
evaluate whether there are MISSED items; ignore other mistakes or extra items.
"""

extra_items_instructions = """
Score 0 if the sample evaluation extracted any extra items from the receipt; otherwise
score 1.

The line items are permitted to have small differences or extraction mistakes, but each
item from the actual receipt must be present in some form in the model's output. Only
evaluate whether there are EXTRA items; ignore other mistakes or missed items.
"""

item_mistakes_instructions = """
Score 0 to 10 based on the number and severity of mistakes in the line items.

A score of 10 means that the two lists are perfectly identical.

Remove 1 point for each minor mistake (typos, capitalization, category name
differences), and up to 3 points for significant mistakes (incorrect quantity, price, or
total, or categories that are not at all similar).
"""

item_extraction_graders = [
    {
        "name": "Missed Line Items",
        "type": "score_model",
        "model": "o4-mini",
        "input": [
            {
                "role": "system",
                "content": item_extraction_base + missed_items_instructions,
            }
        ],
        "range": [0, 1],
        "pass_threshold": 1,
    },
    {
        "name": "Extra Line Items",
        "type": "score_model",
        "model": "o4-mini",
        "input": [
            {
                "role": "system",
                "content": item_extraction_base + extra_items_instructions,
            }
        ],
        "range": [0, 1],
        "pass_threshold": 1,
    },
    {
        "name": "Item Mistakes",
        "type": "score_model",
        "model": "o4-mini",
        "input": [
            {
                "role": "system",
                "content": item_extraction_base + item_mistakes_instructions,
            }
        ],
        "range": [0, 10],
        "pass_threshold": 8,
    },
]


simple_audit_graders = [
    {
        "name": "Not Travel Related Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_audit_decision.not_travel_related }}",
        "reference": "{{ item.correct_audit_decision.not_travel_related }}",
    },
    {
        "name": "Amount Over Limit Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_audit_decision.amount_over_limit }}",
        "reference": "{{ item.correct_audit_decision.amount_over_limit }}",
    },
    {
        "name": "Math Error Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_audit_decision.math_error }}",
        "reference": "{{ item.correct_audit_decision.math_error }}",
    },
    {
        "name": "Handwritten X Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_audit_decision.handwritten_x }}",
        "reference": "{{ item.correct_audit_decision.handwritten_x }}",
    },
    {
        "name": "Needs Audit Accuracy",
        "type": "string_check",
        "operation": "eq",
        "input": "{{ item.predicted_audit_decision.needs_audit }}",
        "reference": "{{ item.correct_audit_decision.needs_audit }}",
    },
]


reasoning_eval_prompt = """
Your task is to evaluate the quality of *reasoning* for audit decisions on receipts.
Here are the rules for audit decisions:

Expenses should be audited if they violate any of the following criteria:
1. Expenses must be travel-related
2. Expenses must not exceed $50
3. All math should be correct; the line items plus tax should equal the total
4. There must not be an "X" in the handwritten notes

If ANY of those criteria are violated, the expense should be audited.

Here is the input to the grader:
{{ item.predicted_receipt_details }}

Below is the output of an authoritative grader making a decision about whether or not to
audit an expense. This is a correct reference decision.

GROUND TRUTH:
{{ item.correct_audit_decision }}


Here is the output of the model we are evaluating:

MODEL GENERATED:
{{ item.predicted_audit_decision }}


Evaluate:
1. For each of the 4 criteria, did the model correctly score it as TRUE or FALSE?
2. Based on the model's *scoring* of the criteria (regardless if it scored it
   correctly), did the model reason appropriately about the criteria (i.e. did it
   understand and apply the prompt correctly)?
3. Is the model's reasoning logically sound, sufficient, and comprehensible?
4. Is the model's reasoning concise, without extraneous details?
5. Is the final decision to audit or not audit correct?

Grade the model with the following rubric:
- (1) point for each of the 4 criteria that the model scored correctly
- (3) points for each aspect of the model's reasoning that is meets the criteria
- (3) points for the model's final decision to audit or not audit

The total score is the sum of the points, and should be between 0 and 10 inclusive.
"""


model_judgement_graders = [
    {
        "name": "Audit Reasoning Quality",
        "type": "score_model",
        "model": "o4-mini",
        "input": [{"role": "system", "content": reasoning_eval_prompt}],
        "range": [0, 10],
        "pass_threshold": 8,
    },
]

full_eval = await create_eval(
    "Full Receipt Processing Evaluation",
    simple_extraction_graders
    + item_extraction_graders
    + simple_audit_graders
    + model_judgement_graders,
)

eval_run = await client.evals.runs.create(
    name="complete-receipt-processing-run",
    eval_id=full_eval.id,
    data_source={
        "type": "jsonl",
        "source": {"type": "file_content", "content": file_content},
    },
)

eval_run.report_url

first_ai_system_cost = calculate_costs(
    fp_rate=1 / 12, fn_rate=1 / 8, per_receipt_cost=0.01
)

print(f"First version of our system, estimated cost: ${first_ai_system_cost:,.0f}")

nursery_receipt_details = ReceiptDetails(
    merchant="WESTERN SIERRA NURSERY",
    location=Location(city="Oakhurst", state="CA", zipcode="93644"),
    time="2024-09-27T12:33:38",
    items=[
        LineItem(
            description="Plantskydd Repellent RTU 1 Liter",
            product_code=None,
            category="Garden/Pest Control",
            item_price="24.99",
            sale_price=None,
            quantity="1",
            total="24.99",
        )
    ],
    subtotal="24.99",
    tax="1.94",
    total="26.93",
    handwritten_notes=[],
)

nursery_audit_decision = AuditDecision(
    not_travel_related=True,
    amount_over_limit=False,
    math_error=False,
    handwritten_x=False,
    reasoning="""
    1. The merchant is a plant nursery and the item purchased an insecticide, so this
       purchase is not travel-related (criterion 1 violated).
    2. The total is $26.93, under $50, so criterion 2 is not violated.
    3. The line items (1 * $24.99 + $1.94 tax) sum to $26.93, so criterion 3 is not
       violated.
    4. There are no handwritten notes or 'X's, so criterion 4 is not violated.
    Since NOT_TRAVEL_RELATED is true, the receipt must be audited.
    """,
    needs_audit=True,
)

flying_j_details = ReceiptDetails(
    merchant="Flying J #616",
    location=Location(city="Frazier Park", state="CA", zipcode=None),
    time="2024-10-01T13:23:00",
    items=[
        LineItem(
            description="Unleaded",
            product_code=None,
            category="Fuel",
            item_price="4.459",
            sale_price=None,
            quantity="11.076",
            total="49.39",
        )
    ],
    subtotal="49.39",
    tax=None,
    total="49.39",
    handwritten_notes=["yos -> home sequoia", "236660"],
)
flying_j_audit_decision = AuditDecision(
    not_travel_related=False,
    amount_over_limit=False,
    math_error=False,
    handwritten_x=False,
    reasoning="""
    1. The only item purchased is Unleaded gasoline, which is travel-related so
       NOT_TRAVEL_RELATED is false.
    2. The total is $49.39, which is under $50, so AMOUNT_OVER_LIMIT is false.
    3. The line items ($4.459 * 11.076 = $49.387884) sum to the total of $49.39, so
       MATH_ERROR is false.
    4. There is no "X" in the handwritten notes, so HANDWRITTEN_X is false.
    Since none of the criteria are violated, the receipt does not need auditing.
    """,
    needs_audit=False,
)

engine_oil_details = ReceiptDetails(
    merchant="O'Reilly Auto Parts",
    location=Location(city="Sylmar", state="CA", zipcode="91342"),
    time="2024-04-26T8:43:11",
    items=[
        LineItem(
            description="VAL 5W-20",
            product_code=None,
            category="Auto",
            item_price="12.28",
            sale_price=None,
            quantity="1",
            total="12.28",
        )
    ],
    subtotal="12.28",
    tax="1.07",
    total="13.35",
    handwritten_notes=["vista -> yos"],
)
engine_oil_audit_decision = AuditDecision(
    not_travel_related=False,
    amount_over_limit=False,
    math_error=False,
    handwritten_x=False,
    reasoning="""
    1. The only item purchased is engine oil, which might be required for a vehicle
       while traveling, so NOT_TRAVEL_RELATED is false.
    2. The total is $13.35, which is under $50, so AMOUNT_OVER_LIMIT is false.
    3. The line items ($12.28 + $1.07 tax) sum to the total of $13.35, so
       MATH_ERROR is false.
    4. There is no "X" in the handwritten notes, so HANDWRITTEN_X is false.
    None of the criteria are violated so the receipt does not need to be audited.
    """,
    needs_audit=False,
)

examples = [
    {"input": nursery_receipt_details, "output": nursery_audit_decision},
    {"input": flying_j_details, "output": flying_j_audit_decision},
    {"input": engine_oil_details, "output": engine_oil_audit_decision},
]

# Format the examples as JSON, with each example wrapped in XML tags.
example_format = """
<example>
    <input>
        {input}
    </input>
    <output>
        {output}
    </output>
</example>
"""

examples_string = ""
for example in examples:
    example_input = example["input"].model_dump_json()
    correct_output = example["output"].model_dump_json()
    examples_string += example_format.format(input=example_input, output=correct_output)

audit_prompt = f"""
Evaluate this receipt data to determine if it need to be audited based on the following
criteria:

1. NOT_TRAVEL_RELATED:
   - IMPORTANT: For this criterion, travel-related expenses include but are not limited
   to: gas, hotel, airfare, or car rental.
   - If the receipt IS for a travel-related expense, set this to FALSE.
   - If the receipt is NOT for a travel-related expense (like office supplies), set this
   to TRUE.
   - In other words, if the receipt shows FUEL/GAS, this would be FALSE because gas IS
   travel-related.
   - Travel-related expenses include anything that could be reasonably required for
   business-related travel activities. For instance, an employee using a personal
   vehicle might need to change their oil; if the receipt is for an oil change or the
   purchase of oil from an auto parts store, this would be acceptable and counts as a
   travel-related expense.

2. AMOUNT_OVER_LIMIT: The total amount exceeds $50

3. MATH_ERROR: The math for computing the total doesn't add up (line items don't sum to
   total)
   - Add up the price and quantity of each line item to get the subtotal
   - Add tax to the subtotal to get the total
   - If the total doesn't match the amount on the receipt, this is a math error
   - If the total is off by no more than $0.01, this is NOT a math error

4. HANDWRITTEN_X: There is an "X" in the handwritten notes

For each criterion, determine if it is violated (true) or not (false). Provide your
reasoning for each decision, and make a final determination on whether the receipt needs
auditing. A receipt needs auditing if ANY of the criteria are violated.

Note that violation of a criterion means that it is `true`. If any of the above four
values are `true`, then the receipt needs auditing (`needs_audit` should be `true`: it
functions as a boolean OR over all four criteria).

If the receipt contains non-travel expenses, then NOT_TRAVEL_RELATED should be `true`
and therefore NEEDS_AUDIT must also be set to `true`. IF THE RECEIPT LISTS ITEMS THAT
ARE NOT TRAVEL-RELATED, THEN IT MUST BE AUDITED. Here are some example inputs to
demonstrate how you should act:

<examples>
{examples_string}
</examples>

Return a structured response with your evaluation.
"""

file_content = await create_dataset_content(receipt_image_dir)

eval_run = await client.evals.runs.create(
    name="updated-receipt-processing-run",
    eval_id=full_eval.id,
    data_source={
        "type": "jsonl",
        "source": {"type": "file_content", "content": file_content},
    },
)

eval_run.report_url

file_content = await create_dataset_content(receipt_image_dir, model="gpt-4.1-mini")

eval_run = await client.evals.runs.create(
    name="receipt-processing-run-gpt-4-1-mini",
    eval_id=full_eval.id,
    data_source={
        "type": "jsonl",
        "source": {"type": "file_content", "content": file_content},
    },
)

eval_run.report_url

system_cost_4_1_mini = calculate_costs(
    fp_rate=1 / 12, fn_rate=0, per_receipt_cost=0.003
)

print(f"Cost using gpt-4.1-mini: ${system_cost_4_1_mini:,.0f}")