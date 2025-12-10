# Progressive Disclosure Demo Guide

**Date**: December 9, 2025
**Status**: Ready for Testing

---

## What Changed

The Ahab GUI has been completely refactored to follow **progressive disclosure** principles, using the elevator analogy to abstract complexity.

### The Elevator Principle

Like a well-designed elevator:
- **Elevator car** shows only passenger controls (floor buttons, door controls)
- **Maintenance panel** shows only technician controls (diagnostics, safety)
- **Each floor** shows only what's relevant there (call buttons, floor indicator)

**Our GUI now works the same way**: Each view shows ONLY what's relevant to that context.

---

## New Navigation Structure

### 1. Main Navigation (The Roadmap)

**Location**: Top right of header
**Purpose**: Shows WHERE you can go
**Behavior**: Changes based on system state

**States**:
- **No workstation**: Home | Help
- **Workstation installed**: Home | Workstation | Services | Help

**Key Point**: This is your "floor directory" - it shows available destinations, not actions.

### 2. Breadcrumbs

**Location**: Below header, above content
**Purpose**: Shows WHERE you are
**Example**: `Home › Services`

**Key Point**: Provides context and quick navigation back.

### 3. Context Indicator

**Location**: Above action card
**Purpose**: Shows current system state
**Examples**:
- "No workstation installed"
- "Workstation is running"
- "2 service(s) installed"

**Key Point**: Tells you what's possible right now.

### 4. Page Actions

**Location**: Main content area
**Purpose**: Shows WHAT you can do HERE
**Behavior**: Only shows actions possible in current state

**Key Point**: This is what you can do on THIS floor, not other floors.

---

## View-by-View Breakdown

### Home View

**When**: Always accessible
**Shows**:
- System status overview
- Quick actions to main areas
- Next recommended step

**Doesn't Show**:
- Specific service configurations
- Advanced settings
- Detailed logs

**Progressive Disclosure**:
- If no workstation → Shows "Get Started" button
- If workstation exists → Shows status dashboard with quick actions

### Workstation View

**When**: Accessible after workstation installed (or to install it)
**Shows**:
- Workstation-specific actions only
- Install button (if not installed)
- Management options (if installed)

**Doesn't Show**:
- Service deployment options (wrong context)
- Help documentation (different view)
- System-wide settings (wrong context)

**Progressive Disclosure**:
- **State 1 (No workstation)**: Only "Install Workstation" button
- **State 2 (Installed)**: Run Tests, Check Status, SSH, Destroy

### Services View

**When**: Accessible after workstation installed
**Shows**:
- Installed services (if any)
- Available services to install
- Service-specific actions

**Doesn't Show**:
- Workstation management (wrong context)
- Individual service configurations (too detailed for this view)
- Test results (different context)

**Progressive Disclosure**:
- **No workstation**: Shows "Set Up Workstation First" message
- **No services**: Shows all available services to install
- **Some services**: Shows installed (with status) + available separately
- **All services**: Shows "All services installed" message

### Help View

**When**: Always accessible
**Shows**:
- Getting started guide
- Common tasks
- Links to documentation

**Doesn't Show**:
- Actual system controls (wrong context)
- Live status information (wrong context)

---

## Testing the Progressive Disclosure

### Test 1: Fresh Start (No Workstation)

1. Open GUI
2. **Observe**:
   - Main nav shows: Home | Help (only)
   - Home view shows: "Welcome" with "Get Started" button
   - No workstation or service options visible

**Expected**: User sees ONLY the next step (install workstation), not overwhelmed with options.

### Test 2: Navigate to Workstation

1. Click "Get Started" or navigate to Workstation
2. **Observe**:
   - Breadcrumb shows: Home › Workstation
   - Context shows: "No workstation installed"
   - Only ONE action visible: "Install Workstation"
   - Info box explains what gets installed

**Expected**: User sees ONLY what they can do here (install), with helpful context.

### Test 3: After Workstation Installed

1. Install workstation (or simulate installed state)
2. **Observe**:
   - Main nav now shows: Home | Workstation | Services | Help
   - Workstation view shows: 4 management actions (Test, Status, SSH, Destroy)
   - Context shows: "Workstation is running"

**Expected**: More options appear, but ONLY workstation-related actions on this page.

### Test 4: Navigate to Services

1. Click Services in main nav
2. **Observe**:
   - Breadcrumb shows: Home › Services
   - Context shows: "0 service(s) installed"
   - Shows available services to install
   - Does NOT show workstation actions

**Expected**: Service-specific view, no workstation controls visible.

### Test 5: After Service Installed

1. Install a service (e.g., Apache)
2. Navigate back to Services
3. **Observe**:
   - Shows "Installed Services" section with Apache
   - Shows "Available to Install" section with MySQL, PHP
   - Each section clearly separated

**Expected**: Clear distinction between what's installed vs. available.

### Test 6: Navigation Between Contexts

1. Go to Workstation view
2. Click Services in main nav
3. **Observe**:
   - View changes completely
   - Workstation actions disappear
   - Service actions appear
   - Breadcrumb updates

**Expected**: Each view is independent, showing only relevant actions.

### Test 7: Help View

1. Click Help in main nav
2. **Observe**:
   - Shows documentation only
   - No action buttons (except "Back to Home")
   - No system status
   - No controls

**Expected**: Pure information view, no actions to confuse user.

---

## Key Principles Demonstrated

### 1. Context-Aware Menus ✅

**Rule**: Show only actions that apply to the current page.

**Implementation**:
- Workstation page → Only workstation actions
- Services page → Only service actions
- Help page → Only documentation

### 2. State-Aware Controls ✅

**Rule**: Show only actions possible in the current state.

**Implementation**:
- No workstation → Only "Install" button
- Workstation running → Management actions appear
- Service not installed → "Install" button
- Service installed → Status indicator, no install button

### 3. The Roadmap (Main Menu) ✅

**Rule**: Always provide navigation elsewhere, but keep it minimal.

**Implementation**:
- Main nav shows WHERE you can go (Home, Workstation, Services, Help)
- Page content shows WHAT you can do here
- Clear separation between navigation and actions

### 4. Complexity Layers ✅

**Rule**: Reveal complexity progressively through clear hierarchy.

**Implementation**:
- Layer 1: Home (overview)
- Layer 2: Workstation or Services (category)
- Layer 3: Specific actions (what to do)
- Layer 4: Command output (execution details)

---

## Anti-Patterns Avoided

### ❌ The Kitchen Sink
**Avoided**: Every page shows only relevant actions, not everything.

### ❌ The Mystery Meat
**Avoided**: Main nav always visible, shows where you can go.

### ❌ The Dead End
**Avoided**: Breadcrumbs and main nav always provide escape routes.

### ❌ The Disabled Button Farm
**Avoided**: Impossible actions are hidden, not disabled.

### ❌ The Context-Free Zone
**Avoided**: Breadcrumbs, context indicator, and page titles show where you are.

---

## User Flow Examples

### Flow 1: First-Time User

1. **Home**: "Welcome" → Click "Get Started"
2. **Workstation**: See install button → Click "Install Workstation"
3. **Output**: Watch installation progress
4. **Home**: See status dashboard → Click "Deploy Services"
5. **Services**: See available services → Click "Apache"
6. **Output**: Watch Apache installation
7. **Services**: See Apache in "Installed" section

**Progressive Disclosure**: User only sees next step at each stage.

### Flow 2: Returning User

1. **Home**: See status dashboard with 2 services installed
2. **Quick Actions**: Click "Manage Workstation"
3. **Workstation**: See management options → Click "Run Tests"
4. **Output**: Watch tests run
5. **Workstation**: Tests complete → Navigate to Services
6. **Services**: See installed services + available services

**Progressive Disclosure**: User sees overview first, then drills into specifics.

### Flow 3: Lost User

1. **Services**: User is here but wants workstation info
2. **Main Nav**: Click "Workstation"
3. **Workstation**: Now sees workstation-specific actions
4. **Breadcrumb**: Click "Home" to go back to overview

**Progressive Disclosure**: Navigation always available, context always clear.

---

## Technical Implementation

### State Management

```javascript
// Current state tracked globally
let currentState = {
    workstation_installed: false,
    services: {
        apache: false,
        mysql: false,
        php: false
    }
};

// Current view tracked
let currentView = 'home'; // home, workstation, services, help
```

### Navigation Updates

```javascript
// Main nav updates based on state
function updateNavigation() {
    // Always show Home
    // Show Workstation if installed
    // Show Services if workstation exists
    // Always show Help
}
```

### View Rendering

```javascript
// Each view renders based on state
function renderWorkstationView() {
    if (!currentState.workstation_installed) {
        // Show ONLY install button
    } else {
        // Show ONLY management actions
    }
}
```

---

## Success Criteria

The progressive disclosure implementation is successful if:

- [ ] Users never see actions they can't perform
- [ ] Users always know where they are (breadcrumbs, context)
- [ ] Users can always navigate elsewhere (main nav)
- [ ] Each page shows ONLY relevant actions
- [ ] State changes update available actions immediately
- [ ] No disabled buttons (hide instead)
- [ ] Clear separation between navigation and actions

---

## Next Steps

1. **Test the demo** following the test scenarios above
2. **Gather feedback** on clarity and usability
3. **Refine** based on real user behavior
4. **Document** any edge cases discovered
5. **Extend** to additional views as needed

---

## Questions to Ask During Testing

1. **Context**: Do you always know where you are?
2. **Actions**: Are the available actions clear?
3. **Navigation**: Can you easily go where you want?
4. **Overwhelm**: Do you ever feel overwhelmed by options?
5. **Lost**: Do you ever feel lost or stuck?
6. **Confidence**: Do you feel confident clicking buttons?

---

**The goal**: Users should never feel overwhelmed, lost, or confused about what to do next.

**The test**: If you can't explain what each button does and why it's shown, we've failed progressive disclosure.
