# Product Requirements Document (PRD)
# Watch Tower - Fleet Management System

**Version:** 1.0  
**Date:** June 27, 2025  
**Author:** VPC Operations Team  
**Status:** In Development

---

## Executive Summary

Watch Tower is an AI-powered fleet management system designed to revolutionize container trucking operations for Virgo Point Capital (VPC) in Lagos, Nigeria. By integrating with LocoNav's GPS tracking system and leveraging natural language processing, Watch Tower transforms complex fleet management tasks into simple conversational commands, reducing operational friction and improving efficiency.

---

## 1. Problem Statement

### 1.1 Current State

Virgo Point Capital operates a fleet of 84+ container trucks moving cargo between ports (primarily ESSLIBRA Terminal) and client locations across Lagos. The current operational workflow suffers from multiple inefficiencies:

#### Pain Points:

1. **Complex Trip Creation Process**
   - Creating trips in LocoNav requires navigating multiple screens
   - Average time to create a single trip: 5-7 minutes
   - Prone to human error in data entry
   - No bulk trip creation capability

2. **Fragmented Data Management**
   - Critical data scattered across LocoNav and Google Sheets
   - No single source of truth for operational metrics
   - Manual data synchronization leading to inconsistencies
   - Time lag between data updates and visibility

3. **Limited Real-time Visibility**
   - Checking truck locations requires logging into LocoNav
   - No quick way to answer "Where is truck X?"
   - Delayed awareness of trip delays or issues
   - No proactive alerts for operational anomalies

4. **Inconsistent Reporting**
   - Manual report generation taking 2-3 hours daily
   - Reports often delayed or missed entirely
   - No standardized performance metrics
   - Difficulty in identifying trends or patterns

5. **Communication Gaps**
   - Information requests go through multiple channels
   - Delays in getting critical operational updates
   - No centralized communication platform for fleet updates
   - Context lost between shifts

### 1.2 Business Impact

These inefficiencies result in:
- **Lost Revenue**: ~15% underutilization of fleet capacity
- **Increased Costs**: 20+ man-hours weekly on manual tasks
- **Delayed Decision Making**: 2-4 hour lag in operational awareness
- **Customer Dissatisfaction**: Inability to provide real-time shipment updates
- **Competitive Disadvantage**: Slower turnaround times compared to competitors

### 1.3 Root Causes

1. **Technology Gap**: Existing tools not designed for conversational interaction
2. **Process Inefficiency**: Manual processes that should be automated
3. **Integration Issues**: Lack of connection between data sources
4. **User Experience**: Complex UIs requiring extensive training

---

## 2. Solution Overview

### 2.1 Vision

Create an intelligent fleet management assistant that enables VPC team members to manage their entire trucking operation through simple natural language commands, providing real-time visibility and automated insights.

### 2.2 Mission

Transform VPC's fleet operations by:
- Reducing trip creation time by 80%
- Providing instant fleet visibility
- Automating routine reporting
- Enabling data-driven decision making

### 2.3 Product Description

Watch Tower is a comprehensive fleet management platform that:

1. **Integrates Multiple Data Sources**
   - Syncs with LocoNav for real-time GPS data
   - Connects to Google Sheets for master data
   - Centralizes all data in a unified database

2. **Provides Natural Language Interface**
   - Slack bot for conversational commands
   - AI-powered query understanding
   - Context-aware responses

3. **Automates Operations**
   - Simplified trip creation
   - Automatic status updates
   - Proactive alert notifications

4. **Delivers Analytics**
   - Real-time performance metrics
   - Daily/weekly summaries
   - Predictive insights

---

## 3. User Personas

### 3.1 Primary Persona: Fleet Operations Manager (Seye)

**Demographics:**
- Role: Fleet Manager
- Experience: 5+ years in logistics
- Technical Skill: Moderate
- Age: 35-45

**Goals:**
- Monitor fleet performance in real-time
- Quickly respond to operational issues
- Reduce manual workload
- Improve fleet utilization

**Pain Points:**
- Spending too much time on data entry
- Difficulty getting quick answers about fleet status
- Manual report generation eating into strategic planning time

**Needs:**
- Simple way to create and track trips
- Instant visibility into truck locations
- Automated daily summaries
- Alerts for critical issues

### 3.2 Secondary Persona: Operations Coordinator (Emmanuel)

**Demographics:**
- Role: Trip Coordinator
- Experience: 2-3 years
- Technical Skill: Basic
- Age: 25-35

**Goals:**
- Create trips efficiently
- Track ongoing deliveries
- Communicate with drivers
- Ensure on-time deliveries

**Pain Points:**
- Complex trip creation process
- No quick way to check trip progress
- Manual tracking of multiple trips
- Difficulty updating trip information

**Needs:**
- Simplified trip creation interface
- Real-time trip tracking
- Easy communication tools
- Quick access to trip history

### 3.3 Tertiary Persona: Senior Management (Anita)

**Demographics:**
- Role: Operations Director
- Experience: 10+ years
- Technical Skill: Basic
- Age: 40-50

**Goals:**
- Optimize overall fleet performance
- Reduce operational costs
- Improve customer satisfaction
- Make data-driven decisions

**Pain Points:**
- Lack of consolidated performance metrics
- Delayed visibility into issues
- Manual compilation of reports
- Difficulty identifying improvement areas

**Needs:**
- Executive dashboards
- Weekly performance summaries
- Trend analysis
- Exception reporting

---

## 4. User Stories

### 4.1 Epic: Fleet Visibility

**As a** fleet manager  
**I want to** quickly check the location and status of any truck  
**So that** I can make informed operational decisions

#### User Stories:
1. Check single truck location via Slack command
2. View all trucks at terminals
3. See trucks at client locations
4. Identify trucks en route
5. Get truck status (operational, maintenance, idle)

### 4.2 Epic: Trip Management

**As an** operations coordinator  
**I want to** create and manage trips through simple commands  
**So that** I can reduce time spent on administrative tasks

#### User Stories:
1. Create trip with natural language command
2. Update trip status
3. Cancel trips
4. View trip progress
5. Get trip tracking URL for customers

### 4.3 Epic: Analytics & Reporting

**As a** senior manager  
**I want to** receive automated performance reports  
**So that** I can identify optimization opportunities

#### User Stories:
1. Receive daily operational summary
2. Get weekly performance metrics
3. View truck utilization reports
4. Analyze turnaround times
5. Track delay patterns

### 4.4 Epic: Alerts & Notifications

**As a** fleet operations team member  
**I want to** receive proactive alerts about issues  
**So that** I can respond quickly to problems

#### User Stories:
1. Get alerts for trip delays
2. Receive geofence entry/exit notifications
3. Be notified of vehicle issues
4. Get driver behavior alerts
5. Receive maintenance reminders

---

## 5. Functional Requirements

### 5.1 Core Features

#### 5.1.1 Natural Language Processing
- **Description**: Understand and process natural language commands
- **Acceptance Criteria**:
  - Parse truck location queries with 95% accuracy
  - Extract trip details from conversational input
  - Handle variations in command structure
  - Provide helpful error messages for unclear commands

#### 5.1.2 Trip Creation
- **Description**: Create trips through Slack commands
- **Acceptance Criteria**:
  - Create trip in <30 seconds
  - Validate all required fields
  - Confirm creation with trip ID
  - Generate tracking URL automatically

#### 5.1.3 Real-time Tracking
- **Description**: Provide current truck locations and status
- **Acceptance Criteria**:
  - Return location within 2 seconds
  - Show last update timestamp
  - Display speed and direction
  - Indicate ignition status

#### 5.1.4 Automated Reporting
- **Description**: Generate and distribute performance reports
- **Acceptance Criteria**:
  - Daily summary at 6 AM Lagos time
  - Weekly report every Monday
  - Include key metrics (TAT, utilization, trips)
  - Deliver via Slack and email

#### 5.1.5 Alert System
- **Description**: Proactive notifications for operational events
- **Acceptance Criteria**:
  - Trip delay alerts (2+ hours late)
  - Geofence entry/exit during active trips
  - Critical alerts within 1 minute
  - Configurable alert preferences

### 5.2 Integration Requirements

#### 5.2.1 LocoNav API Integration
- Real-time GPS data polling (5-minute intervals)
- Webhook handling for instant alerts
- Trip creation and management
- Historical data retrieval

#### 5.2.2 Google Sheets Sync
- Bi-directional data synchronization
- 15-minute sync intervals
- Conflict resolution
- Data validation

#### 5.2.3 Slack Bot
- Slash commands support
- Natural language message handling
- Interactive buttons/modals
- Thread-based conversations

#### 5.2.4 Database
- PostgreSQL via Supabase
- Real-time subscriptions
- Row-level security
- Automated backups

---

## 6. Non-Functional Requirements

### 6.1 Performance
- **Response Time**: <2 seconds for queries
- **Throughput**: Handle 100+ concurrent users
- **Availability**: 99.5% uptime
- **Scalability**: Support up to 500 trucks

### 6.2 Security
- **Authentication**: Token-based API access
- **Encryption**: TLS 1.3 for data in transit
- **Authorization**: Role-based access control
- **Audit**: Complete audit trail of actions

### 6.3 Usability
- **Learning Curve**: <30 minutes training
- **Error Rate**: <5% user errors
- **Satisfaction**: >90% user satisfaction
- **Accessibility**: Mobile-responsive interface

### 6.4 Reliability
- **Data Accuracy**: 99.9% accuracy
- **Sync Reliability**: No data loss during sync
- **Error Recovery**: Automatic retry mechanisms
- **Backup**: Daily automated backups

### 6.5 Compliance
- **Data Privacy**: NDPR compliance
- **Retention**: 6-month data retention
- **Right to Access**: User data export capability
- **Audit Trail**: Complete activity logging

---

## 7. Success Metrics

### 7.1 Operational Metrics
- **Trip Creation Time**: Reduce from 5-7 minutes to <1 minute (85% reduction)
- **Average TAT**: Improve by 20% within 3 months
- **Fleet Utilization**: Increase from 65% to 80%
- **On-time Delivery**: Improve from 75% to 90%

### 7.2 User Adoption Metrics
- **Daily Active Users**: 80% of operations team
- **Commands per Day**: >100 Slack commands
- **Feature Utilization**: All features used weekly
- **User Satisfaction**: NPS score >8

### 7.3 Business Impact Metrics
- **Cost Savings**: ₦2M monthly from efficiency gains
- **Revenue Increase**: 15% from improved utilization
- **Customer Satisfaction**: 20% improvement in CSAT
- **Operational Efficiency**: 30% reduction in manual tasks

### 7.4 Technical Metrics
- **System Uptime**: >99.5%
- **API Response Time**: <500ms p95
- **Data Sync Success**: >99%
- **Error Rate**: <1%

---

## 8. Scope and Constraints

### 8.1 In Scope
- Slack bot interface
- Trip creation and tracking
- Real-time fleet visibility
- Automated reporting
- Basic analytics
- Geofence monitoring
- Alert notifications
- Google Sheets integration

### 8.2 Out of Scope (Phase 1)
- Route optimization
- Fuel management
- Maintenance scheduling
- Driver mobile app
- Customer portal
- Billing integration
- Multi-language support
- Offline functionality

### 8.3 Constraints
- **Technical**: Must integrate with existing LocoNav API
- **Operational**: Cannot disrupt ongoing operations
- **Financial**: Development budget of ₦5M
- **Timeline**: MVP in 4 weeks
- **Resources**: 2 developers, 1 PM

### 8.4 Dependencies
- LocoNav API access and stability
- Google Sheets API quotas
- Slack workspace configuration
- Internet connectivity
- User training availability

---

## 9. Implementation Timeline

### Phase 1: Foundation (Weeks 1-2)
- Database setup and schema
- Basic API structure
- LocoNav integration
- Google Sheets sync
- Simple Slack commands

### Phase 2: Core Features (Weeks 2-3)
- Natural language processing
- Trip creation workflow
- Real-time tracking
- Basic alerts
- Daily summaries

### Phase 3: Enhancement (Weeks 3-4)
- Advanced analytics
- Comprehensive reporting
- Alert customization
- Performance optimization
- User testing

### Phase 4: Launch (Week 4)
- Production deployment
- User training
- Documentation
- Support setup
- Monitoring

---

## 10. Risks and Mitigation

### 10.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| LocoNav API limits | High | Medium | Implement caching and rate limiting |
| Data sync conflicts | Medium | High | Version control and conflict resolution |
| AI accuracy issues | Medium | Medium | Human-in-the-loop validation |
| System downtime | High | Low | Redundancy and monitoring |

### 10.2 Operational Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| User adoption resistance | High | Medium | Extensive training and support |
| Data quality issues | Medium | High | Validation rules and cleanup |
| Process change management | Medium | Medium | Phased rollout approach |
| Integration complexity | High | Low | Incremental implementation |

### 10.3 Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| ROI not achieved | High | Low | Clear metrics and monitoring |
| Scope creep | Medium | High | Strict change management |
| Resource availability | Medium | Medium | Buffer in timeline |
| Competitor response | Low | Low | Rapid iteration capability |

---

## 11. Appendices

### 11.1 Glossary
- **TAT**: Truck Around Time
- **VPC**: Virgo Point Capital
- **ESSLIBRA**: Main port terminal
- **Geofence**: Virtual geographic boundary
- **Trip**: Single delivery journey

### 11.2 References
- LocoNav API Documentation
- Google Sheets API Guide
- Slack Bot Development Guide
- OpenAI Integration Best Practices

### 11.3 Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | June 27, 2025 | VPC Team | Initial version |

---

**Approval Signatures:**

_Product Owner:_ _________________________ Date: _________

_Technical Lead:_ _________________________ Date: _________

_Operations Manager:_ _____________________ Date: _________
