# PROMPT — CREATE RPD.md

## Resource Production and Design Documentation

You are a senior system designer, product designer, technical writer, and production pipeline architect.

Your task is to create a complete, professional, implementation-oriented documentation file:

`RPD.md`

RPD stands for:

**Resource Production and Design**

The document must define how all resources/assets required by this project are designed, produced, organized, validated, optimized, versioned, and released.

Do NOT create a generic explanation.
Create documentation that can actually be used by the development team and AI coding agents during the entire project lifecycle.

---

# 1. RPD OBJECTIVES

Define the objectives of the Resource Production and Design system.

The RPD system must:

* establish a consistent design language
* define resource requirements
* standardize asset creation
* standardize naming conventions
* standardize folder structures
* prevent duplicated resources
* prevent unused resources
* maintain resource quality
* optimize resource size and performance
* support version control
* support collaboration
* support automated validation
* support testing
* support production releases
* make resources easy for developers and designers to find
* make resources easy for AI coding agents to understand and modify

The RPD system must cover the entire lifecycle:

`Concept → Specification → Design → Production → Review → Optimization → Testing → Integration → Release → Maintenance`

---

# 2. RESOURCE CATEGORIES

Define every resource category relevant to the project.

At minimum consider:

## Visual Resources

* UI assets
* icons
* logos
* illustrations
* backgrounds
* textures
* images
* thumbnails
* animations
* visual effects

## Design Resources

* design tokens
* colors
* typography
* spacing
* sizing
* grids
* components
* layouts
* interaction patterns

## Technical Resources

* configuration files
* JSON
* YAML
* schemas
* templates
* metadata
* localization files
* environment configuration

## Audio Resources

If applicable:

* music
* sound effects
* UI sounds
* voice
* ambient sounds

## Documentation Resources

* specifications
* guidelines
* references
* technical documentation
* design documentation

If the project does not use a category, explicitly mark it as:

`N/A`

Do not invent unnecessary resources.

---

# 3. RESOURCE SPECIFICATION

For every resource define a specification.

Each resource specification should contain:

* resource name
* resource ID
* category
* purpose
* description
* source
* owner
* dependencies
* required format
* dimensions
* resolution
* quality requirements
* performance requirements
* accessibility requirements
* licensing requirements
* target platform
* usage location
* version
* status

Recommended status values:

* PLANNED
* DESIGNING
* IN_PRODUCTION
* REVIEW
* APPROVED
* INTEGRATED
* DEPRECATED
* REJECTED

---

# 4. DESIGN SYSTEM

Create a unified design system for resources.

Define:

## Color

* primary
* secondary
* accent
* background
* surface
* text
* border
* success
* warning
* error
* disabled

## Typography

Define:

* font family
* heading hierarchy
* body text
* labels
* captions
* monospace text
* font sizes
* font weights
* line heights
* letter spacing

## Spacing

Define a consistent spacing scale.

Example:

```text
4
8
12
16
24
32
48
64
```

The exact scale may be adapted to the project.

## Components

Define reusable components instead of creating one-off designs.

Examples:

* buttons
* cards
* navigation
* dialogs
* forms
* inputs
* dropdowns
* tabs
* tables
* notifications
* tooltips
* loading states
* empty states
* error states

---

# 5. RESOURCE PRODUCTION PIPELINE

Define the complete production workflow.

Use this pipeline:

```text
Requirement
    ↓
Resource Specification
    ↓
Concept
    ↓
Design
    ↓
Production
    ↓
Self Review
    ↓
Quality Control
    ↓
Optimization
    ↓
Testing
    ↓
Approval
    ↓
Integration
    ↓
Release
```

Explain what happens at every stage.

For each stage define:

* input
* process
* output
* responsible role
* validation
* acceptance criteria

---

# 6. SOURCE FILES VS PRODUCTION FILES

Clearly separate:

```text
source/
production/
final/
```

Define the purpose of each directory.

Example:

```text
resources/
├── source/
│   ├── design/
│   ├── illustrations/
│   ├── 3d/
│   └── audio/
│
├── production/
│   ├── processed/
│   ├── optimized/
│   └── generated/
│
└── final/
    ├── ui/
    ├── images/
    ├── icons/
    └── audio/
```

Source files must never be accidentally overwritten by automated production scripts.

---

# 7. FOLDER STRUCTURE

Design a scalable resource directory.

Use a structure appropriate for the actual project.

Example:

```text
resources/
├── design/
├── ui/
├── icons/
├── images/
├── illustrations/
├── animation/
├── audio/
├── fonts/
├── data/
├── localization/
├── templates/
├── source/
├── generated/
├── optimized/
└── documentation/
```

Explain the purpose of every directory.

Do not create folders without a reason.

---

# 8. NAMING CONVENTION

Create strict naming rules.

Names should:

* be predictable
* be searchable
* avoid unnecessary spaces
* avoid random names
* avoid duplicate names
* support automation

Define conventions for:

* files
* folders
* components
* icons
* images
* audio
* data
* versions

Example:

```text
button-primary.svg
icon-settings.svg
hero-dashboard.webp
menu-click.ogg
dashboard-card.json
```

Avoid:

```text
final.png
final2.png
final-new.png
final-final.png
asdf.png
test123.png
```

---

# 9. RESOURCE ID SYSTEM

Create a unique resource identification system.

Example:

```text
UI-BTN-001
UI-ICON-001
IMG-HERO-001
AUD-SFX-001
DATA-CONFIG-001
```

Explain:

* category prefix
* resource type
* numeric ID
* optional variant

Resource IDs must never be reused after deletion.

---

# 10. VERSIONING

Define resource versioning.

Use semantic versioning where appropriate:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.0.0
1.1.0
1.1.1
2.0.0
```

Explain when to increment:

* MAJOR
* MINOR
* PATCH

Also define how resource changes should be documented.

---

# 11. QUALITY CONTROL

Create a Resource QA checklist.

Check:

### Design

* correct dimensions
* correct spacing
* correct typography
* correct colors
* consistent visual style
* correct alignment
* correct component usage

### Technical

* valid file format
* valid metadata
* no corrupted files
* correct naming
* correct location
* correct permissions
* no unnecessary dependencies

### Performance

* optimized file size
* appropriate compression
* no unnecessary high-resolution assets
* no duplicate resources
* no unused resources

### Accessibility

Where applicable:

* sufficient contrast
* readable typography
* alternative text
* meaningful labels
* keyboard accessibility
* screen-reader compatibility

---

# 12. OPTIMIZATION

Define resource optimization rules.

Examples:

Images:

* use SVG for scalable vector graphics
* use WebP/AVIF where appropriate
* avoid unnecessarily huge images
* compress production images

Icons:

* prefer SVG
* remove unnecessary metadata
* optimize paths

Audio:

* use appropriate bitrate
* avoid unnecessary high-resolution audio
* normalize volume where appropriate

Code/data:

* minify production resources when appropriate
* remove development-only data
* validate schemas

Optimization must NEVER reduce quality below the project's acceptance criteria.

---

# 13. RESOURCE VALIDATION

Create automated validation requirements.

The project should be able to detect:

* missing resources
* invalid filenames
* duplicate resources
* broken references
* unsupported formats
* invalid metadata
* unused resources
* oversized assets
* incorrect dimensions
* invalid JSON/YAML
* missing required fields

If possible, define scripts such as:

```bash
./tools/rpd validate
./tools/rpd check
./tools/rpd optimize
./tools/rpd report
```

The AI coding agent should implement these tools if the project architecture supports them.

---

# 14. DESIGN REVIEW

Define a review process.

Every important resource should pass:

```text
Creator Review
      ↓
Technical Review
      ↓
Design Review
      ↓
Final Approval
```

Define rejection reasons.

Examples:

* inconsistent design
* poor quality
* wrong dimensions
* wrong naming
* performance issue
* accessibility issue
* licensing issue
* unnecessary resource

---

# 15. RESOURCE DEPENDENCY MANAGEMENT

Document relationships between resources.

Example:

```text
Dashboard
 ├── dashboard-background.webp
 ├── icon-server.svg
 ├── icon-storage.svg
 └── dashboard-card.json
```

The system must make it possible to determine:

* what uses a resource
* what resources a component requires
* whether deleting a resource will break something

Never delete a resource blindly.

---

# 16. LICENSE AND ATTRIBUTION

Define rules for third-party resources.

Every external resource must document:

* source
* creator
* license
* URL/reference
* modification status
* attribution requirements

Do not use copyrighted resources without proper permission.

Separate:

```text
original/
third-party/
generated/
```

where appropriate.

---

# 17. GENERATED RESOURCES

If AI-generated or automatically generated resources are used, document:

* generation source
* generation method
* prompt/reference
* generation date
* processing steps
* modifications
* final approval

Generated resources must still pass normal QA.

AI-generated does NOT automatically mean production-ready.

---

# 18. DESIGN TOKENS

If applicable, define machine-readable design tokens.

Example:

```json
{
  "color": {
    "primary": "...",
    "background": "...",
    "text": "..."
  },
  "spacing": {
    "sm": 8,
    "md": 16,
    "lg": 24
  }
}
```

The implementation should use tokens instead of repeatedly hardcoding values.

---

# 19. RESPONSIVE DESIGN

If the project has a UI, define resource behavior across:

* desktop
* laptop
* tablet
* mobile
* high-resolution displays

Define:

* breakpoints
* scaling
* image behavior
* component adaptation
* typography scaling

Avoid designing only for one screen size unless the project explicitly targets one platform.

---

# 20. PRODUCTION AUTOMATION

Identify processes that can be automated.

Examples:

```text
asset optimization
image conversion
SVG optimization
metadata validation
duplicate detection
unused-resource detection
resource reports
build generation
resource packaging
```

Automation must be:

* repeatable
* deterministic where possible
* safe
* logged
* reversible

---

# 21. CI/CD INTEGRATION

Define how RPD integrates with CI/CD.

Every production build should optionally run:

```text
RPD validation
↓
Resource integrity check
↓
Optimization check
↓
Reference check
↓
Build
↓
Tests
↓
Release
```

A critical resource validation failure should be able to block a release.

---

# 22. TESTING

Define tests for:

* resource existence
* resource loading
* resource integrity
* visual consistency
* performance
* accessibility
* responsive behavior
* broken references
* duplicate detection

Include unit tests and integration tests where appropriate.

---

# 23. RESOURCE INVENTORY

Create a resource inventory format.

Example:

| ID          | Name           | Type | Location   | Version | Status   | Owner  |
| ----------- | -------------- | ---- | ---------- | ------- | -------- | ------ |
| UI-BTN-001  | Primary Button | UI   | ui/buttons | 1.0.0   | APPROVED | Design |
| UI-ICON-001 | Settings       | Icon | icons      | 1.0.0   | APPROVED | Design |

The inventory should become the source of truth for project resources.

---

# 24. CHANGE MANAGEMENT

Every significant resource change must record:

* what changed
* why it changed
* who changed it
* version
* date
* affected components
* migration requirements

Do not silently replace important production resources.

---

# 25. DEPRECATION

Define how resources are deprecated.

A deprecated resource should:

* be marked clearly
* remain documented
* identify its replacement
* identify affected components
* have a planned removal version

Example:

```text
UI-ICON-014
Status: DEPRECATED
Replacement: UI-ICON-032
Removal: v2.0.0
```

---

# 26. SECURITY

RPD must consider resource security.

Check for:

* malicious files
* executable resources
* unexpected scripts
* unsafe third-party resources
* path traversal
* malicious metadata
* oversized files used for denial-of-service style abuse
* untrusted generated content

Never execute an unknown resource merely because it exists inside the resource directory.

---

# 27. BACKUP AND RECOVERY

Define how source resources are backed up.

Important source files must be recoverable.

Define:

* backup frequency
* version history
* recovery procedure
* archive strategy

Production optimization must never destroy the only source version.

---

# 28. RELEASE PROCESS

Define:

```text
Development
↓
Resource Freeze
↓
Final QA
↓
Optimization
↓
Validation
↓
Build
↓
Release Candidate
↓
Testing
↓
Approval
↓
Production Release
```

Create a release checklist.

---

# 29. RPD STATUS DASHBOARD

Define a simple status overview.

Example:

```text
Total Resources: 152

PLANNED:       12
IN_PRODUCTION: 23
REVIEW:        8
APPROVED:      96
DEPRECATED:    13
```

If the project has a dashboard, explain how this data could be exposed.

---

# 30. AI CODING AGENT RULES

The AI coding agent MUST follow these rules when modifying resources:

1. Inspect existing resources before creating new ones.
2. Never create duplicate resources without justification.
3. Follow RPD naming conventions.
4. Follow the defined folder structure.
5. Update resource inventory when adding important resources.
6. Validate resources after modification.
7. Do not delete production resources blindly.
8. Preserve source files.
9. Explain destructive changes before performing them.
10. Keep generated resources separate from source resources.
11. Update documentation when resource architecture changes.
12. Run relevant RPD validation before declaring the task complete.

---

# 31. DEFINITION OF DONE

A resource is considered complete only when:

* specification exists
* design is approved
* production version exists
* naming is valid
* location is correct
* dependencies are documented
* resource passes QA
* resource is optimized
* resource is tested
* resource inventory is updated
* integration succeeds
* documentation is updated

---

# 32. RPD CHECKLIST

Create a final checklist:

```text
[ ] Requirement defined
[ ] Resource specification created
[ ] Design completed
[ ] Source file preserved
[ ] Production resource generated
[ ] Naming validated
[ ] Format validated
[ ] Dimensions validated
[ ] Optimization completed
[ ] Accessibility checked
[ ] Dependencies checked
[ ] License checked
[ ] Integration tested
[ ] Resource inventory updated
[ ] Documentation updated
[ ] Final approval completed
```

---

# 33. FINAL REQUIREMENT

After creating `RPD.md`, inspect the existing project structure.

Adapt the documentation to the actual project instead of blindly following generic examples.

If existing conventions already exist:

* preserve them where reasonable
* document them
* improve inconsistencies
* avoid unnecessary rewrites

Do NOT fabricate project components that do not exist.

At the end, provide:

1. `RPD.md`
2. recommended resource directory structure
3. recommended validation scripts
4. recommended production workflow
5. identified gaps
6. next implementation steps

The final result must be professional enough to function as the project's official **Resource Production and Design specification**.
