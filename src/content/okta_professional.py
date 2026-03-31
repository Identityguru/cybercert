"""
Okta Certified Professional — complete study content and quiz question bank.

Reference: Okta Professional Study Guide (OIE)
Exam: Okta Certified Professional Hands-On Configuration Exam

Each topic dict contains:
  title             — display title
  icon              — emoji icon
  estimated_minutes — reading time
  summary           — 2–3 sentence overview
  sections          — list of content blocks (heading, body, key_points)
  quiz_questions    — list of MCQs (q, options, answer index, explanation)
  exam_tips         — bullet points for exam-day recall
"""

TOPICS: dict = {

    # ────────────────────────────────────────────────────────────────────────
    # 1. User Lifecycle States
    # ────────────────────────────────────────────────────────────────────────
    "user-lifecycle": {
        "title": "User Lifecycle States",
        "icon": "👤",
        "estimated_minutes": 10,
        "summary": (
            "Okta defines 7 distinct lifecycle states for every user account. "
            "Understanding these states — and the valid transitions between them — "
            "is foundational to managing identities and troubleshooting access issues "
            "in an Okta OIE environment."
        ),
        "sections": [
            {
                "heading": "The 7 Lifecycle States",
                "body": (
                    "Every user in Okta exists in exactly one of these states at any point in time. "
                    "The states control whether a user can authenticate, receive emails, and access apps."
                ),
                "key_points": [
                    "STAGED — User record created but activation not yet initiated. No email sent.",
                    "PROVISIONED — Activation email sent but user has not yet set a password. Also called PENDING_USER_ACTION in some docs.",
                    "ACTIVE — User is fully activated and can authenticate normally.",
                    "RECOVERY — User has requested a password reset. The reset link is valid for a limited time.",
                    "LOCKED_OUT — User exceeded the maximum failed login attempts. Admin or policy must unlock.",
                    "PASSWORD_EXPIRED — Password has passed its maximum age. User must change it on next login.",
                    "DEPROVISIONED — User has been deactivated. Cannot log in; data is retained.",
                ],
            },
            {
                "heading": "Key State Transitions",
                "body": (
                    "Transitions are triggered by admin actions, user actions, or policy enforcement. "
                    "Not all transitions are valid — e.g. you cannot go directly from STAGED to DEPROVISIONED."
                ),
                "key_points": [
                    "STAGED → PROVISIONED: Admin clicks 'Activate' or sends activation email.",
                    "PROVISIONED → ACTIVE: User clicks activation link and sets password.",
                    "ACTIVE → LOCKED_OUT: Exceeds max login failures (policy-defined).",
                    "ACTIVE → PASSWORD_EXPIRED: Password age exceeds max (policy-defined).",
                    "ACTIVE → RECOVERY: User or admin initiates password reset.",
                    "ACTIVE → DEPROVISIONED: Admin deactivates the user.",
                    "DEPROVISIONED → PROVISIONED: Admin reactivates the user (new activation email sent).",
                ],
            },
            {
                "heading": "STAGED vs PROVISIONED — the Critical Distinction",
                "body": (
                    "This is the most commonly tested distinction on the exam. "
                    "STAGED means Okta has the user record but nothing has been sent to the user yet. "
                    "PROVISIONED means the activation email was sent but the user hasn't completed it."
                ),
                "key_points": [
                    "STAGED: Record exists in Okta. No email. User is unaware.",
                    "PROVISIONED: Activation email sent. Awaiting user action.",
                    "PROVISIONED users appear in app assignments but cannot authenticate yet.",
                    "JIT (Just-In-Time) provisioning skips STAGED — users go directly to ACTIVE.",
                ],
            },
            {
                "heading": "DEPROVISIONED vs Deleted",
                "body": (
                    "Deprovisioning is reversible; deletion is permanent. "
                    "DEPROVISIONED users cannot log in but their profile, group memberships, "
                    "and audit history are retained."
                ),
                "key_points": [
                    "DEPROVISIONED users cannot authenticate to any app.",
                    "Reactivating a DEPROVISIONED user sends a new activation email (→ PROVISIONED).",
                    "Deleting a user permanently removes all records — use with caution.",
                    "SCIM-provisioned users are deprovisioned (not deleted) when removed from the source.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "A user's record exists in Okta but they have not yet received an activation email. What is their lifecycle state?",
                "options": ["PROVISIONED", "STAGED", "ACTIVE", "RECOVERY"],
                "answer": 1,
                "explanation": "STAGED means the user record exists in Okta but activation has not been initiated. No email has been sent.",
            },
            {
                "q": "A user clicks the activation link in their email and sets their password. What state do they transition to?",
                "options": ["PROVISIONED", "RECOVERY", "ACTIVE", "PASSWORD_EXPIRED"],
                "answer": 2,
                "explanation": "Completing the activation flow (clicking the link and setting a password) moves the user from PROVISIONED to ACTIVE.",
            },
            {
                "q": "Which lifecycle state indicates a user has exceeded the maximum number of failed login attempts?",
                "options": ["RECOVERY", "DEPROVISIONED", "LOCKED_OUT", "PASSWORD_EXPIRED"],
                "answer": 2,
                "explanation": "LOCKED_OUT occurs when a user exceeds the max failed login attempts defined in the account lockout policy.",
            },
            {
                "q": "An admin deactivates a user. The user's profile and group memberships are retained. What state is the user in?",
                "options": ["STAGED", "DEPROVISIONED", "LOCKED_OUT", "DELETED"],
                "answer": 1,
                "explanation": "DEPROVISIONED users cannot authenticate but their data is retained. Deletion (not a lifecycle state) permanently removes the record.",
            },
            {
                "q": "How many distinct user lifecycle states does Okta define?",
                "options": ["5", "6", "7", "8"],
                "answer": 2,
                "explanation": "Okta defines 7 lifecycle states: STAGED, PROVISIONED, ACTIVE, RECOVERY, LOCKED_OUT, PASSWORD_EXPIRED, and DEPROVISIONED.",
            },
            {
                "q": "A DEPROVISIONED user needs to regain access. An admin reactivates them. What state do they transition to?",
                "options": ["ACTIVE", "STAGED", "PROVISIONED", "RECOVERY"],
                "answer": 2,
                "explanation": "Reactivating a DEPROVISIONED user sends a new activation email, moving them to PROVISIONED. They become ACTIVE once they complete activation.",
            },
            {
                "q": "Which state is a user in when they have requested a password reset but have not yet completed it?",
                "options": ["LOCKED_OUT", "PASSWORD_EXPIRED", "RECOVERY", "PROVISIONED"],
                "answer": 2,
                "explanation": "RECOVERY is the state during an active password reset. The reset link has a time limit defined by policy.",
            },
        ],
        "exam_tips": [
            "STAGED = record exists, no email sent. PROVISIONED = email sent, not yet activated.",
            "7 states: STAGED, PROVISIONED, ACTIVE, RECOVERY, LOCKED_OUT, PASSWORD_EXPIRED, DEPROVISIONED.",
            "DEPROVISIONED retains data; deletion is permanent and irreversible.",
            "JIT provisioning bypasses STAGED — users activate directly to ACTIVE.",
            "Only ACTIVE users can authenticate to apps.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 2. Policy Evaluation Order
    # ────────────────────────────────────────────────────────────────────────
    "policy-evaluation": {
        "title": "Policy Evaluation Order",
        "icon": "📋",
        "estimated_minutes": 8,
        "summary": (
            "Okta evaluates sign-on and password policies in a strict priority order. "
            "Understanding how policies and rules are ranked — and how the catch-all default "
            "works — is essential for designing access controls and troubleshooting unexpected behaviour."
        ),
        "sections": [
            {
                "heading": "Policy Types",
                "body": (
                    "Okta uses several policy types, each serving a different purpose. "
                    "The most exam-relevant are Okta Sign-On Policy and Password Policy."
                ),
                "key_points": [
                    "Okta Sign-On Policy — controls MFA and session behaviour for the Okta dashboard.",
                    "App Sign-On Policy (Authentication Policy in OIE) — controls access to a specific application.",
                    "Password Policy — governs password complexity, age, and lockout for a group of users.",
                    "Profile Enrollment Policy — determines self-registration and profile attributes.",
                    "MFA Enrollment Policy — determines which factors users must enrol in OIE.",
                ],
            },
            {
                "heading": "Priority-Based Evaluation",
                "body": (
                    "Policies are evaluated in ascending priority order (lowest number = highest priority). "
                    "The first policy whose conditions match the user wins — Okta does not continue evaluating."
                ),
                "key_points": [
                    "Priority 1 is the most restrictive / specific policy and evaluated first.",
                    "The Default Policy always has the lowest priority and acts as a catch-all.",
                    "Each policy contains one or more rules, also evaluated by priority.",
                    "Within a policy, the first matching rule is applied — no further rules are checked.",
                    "The Default Rule in every policy matches all users not matched by a higher rule.",
                ],
            },
            {
                "heading": "Policy Scope: Org-level vs App-level",
                "body": (
                    "In OIE, sign-on policies are app-level (Authentication Policies), not org-level. "
                    "Each application has its own Authentication Policy with independent rules."
                ),
                "key_points": [
                    "Classic Okta: single Okta Sign-On Policy applies org-wide.",
                    "OIE: each app has its own Authentication Policy — more granular control.",
                    "Okta Sign-On Policy still exists in OIE but governs Okta dashboard access.",
                    "Password Policies are group-scoped: assign the policy to specific groups.",
                    "A user in multiple groups follows the password policy with the highest priority assigned to their group.",
                ],
            },
            {
                "heading": "Rule Conditions and Actions",
                "body": (
                    "Each rule has conditions (who it applies to) and actions (what to do). "
                    "Rules support conditions like group membership, network zone, device state, and authenticator state."
                ),
                "key_points": [
                    "Conditions: User is in group X, accessing from network zone Y, on managed device.",
                    "Actions: Allow, Deny, require MFA, set session lifetime, require re-authentication.",
                    "In OIE Authentication Policies, actions use an Assurance model with factor requirements.",
                    "A DENY action blocks access; the user receives an error, not an MFA prompt.",
                    "Network zones must be pre-defined before being referenced in a rule condition.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "Okta evaluates multiple sign-on policies. Which policy is evaluated first?",
                "options": [
                    "The policy with the highest priority number",
                    "The Default Policy",
                    "The policy with the lowest priority number",
                    "Policies are evaluated alphabetically",
                ],
                "answer": 2,
                "explanation": "Okta evaluates policies in ascending priority order — priority 1 (lowest number) is evaluated first. The first matching policy wins.",
            },
            {
                "q": "What is the purpose of the Default Policy in Okta?",
                "options": [
                    "It restricts all users not matched by other policies",
                    "It acts as a catch-all for users not matched by any higher-priority policy",
                    "It is the only policy that applies to admin users",
                    "It defines the org-wide MFA requirement",
                ],
                "answer": 1,
                "explanation": "The Default Policy has the lowest priority and is evaluated last. It catches all users not matched by higher-priority policies.",
            },
            {
                "q": "In Okta Identity Engine (OIE), where are sign-on policies configured?",
                "options": [
                    "At the org level only",
                    "At the app level as Authentication Policies",
                    "At the group level only",
                    "In the Universal Directory",
                ],
                "answer": 1,
                "explanation": "In OIE, each application has its own Authentication Policy. This enables per-app access control rather than a single org-wide policy.",
            },
            {
                "q": "A user matches rule 3 in a sign-on policy. Rules 1 and 2 did not match. What happens?",
                "options": [
                    "All three rules are applied cumulatively",
                    "Only rule 3's action is applied; no further rules are evaluated",
                    "The Default Rule overrides rule 3",
                    "The user is denied access because multiple rules were skipped",
                ],
                "answer": 1,
                "explanation": "Okta stops evaluating once the first matching rule is found. Rule 3's action is applied and no further rules in the policy are checked.",
            },
            {
                "q": "A Password Policy is assigned to two groups. User A is in both groups. Which policy applies?",
                "options": [
                    "Both policies apply simultaneously",
                    "The policy assigned to the group with the higher priority",
                    "The most recently created policy",
                    "The Default Password Policy always takes precedence",
                ],
                "answer": 1,
                "explanation": "When a user belongs to multiple groups with different password policies, the policy assigned to the group with the highest priority (lowest number) applies.",
            },
        ],
        "exam_tips": [
            "Lower priority number = higher precedence. Priority 1 is evaluated first.",
            "First matching policy/rule wins — evaluation stops immediately.",
            "Default Policy / Default Rule = catch-all, always lowest priority.",
            "OIE: Authentication Policies are per-app. Classic Okta: single org-level Sign-On Policy.",
            "DENY is an explicit block — the user will not be prompted for MFA.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 3. SAML vs OIDC
    # ────────────────────────────────────────────────────────────────────────
    "saml-vs-oidc": {
        "title": "SAML vs OIDC Key Terms",
        "icon": "🔑",
        "estimated_minutes": 12,
        "summary": (
            "SAML 2.0 and OpenID Connect (OIDC) are the two dominant SSO protocols. "
            "The exam tests your ability to identify key terms, roles, and token/assertion types "
            "for each protocol and understand when to use one over the other."
        ),
        "sections": [
            {
                "heading": "SAML 2.0 Key Terms",
                "body": (
                    "SAML uses XML-based assertions passed between an Identity Provider and a Service Provider. "
                    "It is widely used for enterprise SSO to web applications."
                ),
                "key_points": [
                    "Identity Provider (IdP) — authenticates the user and issues the SAML assertion (Okta is the IdP).",
                    "Service Provider (SP) — the application that relies on Okta to authenticate users.",
                    "SAML Assertion — XML document containing statements about the user (authentication, attribute, authorization).",
                    "Metadata — XML file exchanged between IdP and SP to establish trust (contains certificates, endpoints).",
                    "ACS URL (Assertion Consumer Service) — the SP endpoint that receives the SAML assertion via POST.",
                    "Entity ID — unique identifier for the IdP or SP in the metadata.",
                    "Audience Restriction — limits which SP can use the assertion (prevents relay attacks).",
                    "SP-initiated flow — user starts at the SP, is redirected to Okta, then back to SP with assertion.",
                    "IdP-initiated flow — user starts at Okta, clicks the app tile, assertion is posted to SP.",
                ],
            },
            {
                "heading": "OIDC Key Terms",
                "body": (
                    "OIDC (OpenID Connect) is built on OAuth 2.0 and uses JSON Web Tokens (JWTs). "
                    "It is the modern protocol for web and mobile apps."
                ),
                "key_points": [
                    "Authorization Server — Okta's OAuth 2.0 server that issues tokens.",
                    "Client (Relying Party) — the application that requests authentication from Okta.",
                    "ID Token — JWT containing claims about the authenticated user (who they are).",
                    "Access Token — JWT or opaque token granting access to an API (what they can do).",
                    "Refresh Token — long-lived token used to get new access/ID tokens without re-authentication.",
                    "Claims — key-value pairs in a JWT (sub, email, name, groups, etc.).",
                    "Scopes — permissions requested by the client (openid, profile, email, groups).",
                    "Authorization Code flow — most secure; code exchanged for tokens server-side (use for web apps).",
                    "PKCE (Proof Key for Code Exchange) — extension to Authorization Code flow for public clients (SPAs, mobile).",
                ],
            },
            {
                "heading": "SAML vs OIDC Comparison",
                "body": (
                    "Choosing between SAML and OIDC depends on the application type and protocol support. "
                    "Okta supports both as an IdP."
                ),
                "key_points": [
                    "SAML: XML-based, older, enterprise web apps, assertion = XML document.",
                    "OIDC: JSON/JWT-based, modern, web + mobile + API, assertion = ID Token.",
                    "SAML uses HTTP POST/Redirect bindings; OIDC uses HTTP redirects + JSON endpoints.",
                    "OIDC is preferred for new integrations; SAML for legacy enterprise apps.",
                    "Both support SSO, but only OIDC natively supports API authorization (via OAuth 2.0).",
                    "Okta acts as IdP for SAML and as both Authorization Server and IdP for OIDC.",
                ],
            },
            {
                "heading": "Configuring SAML Apps in Okta",
                "body": "Key fields required when setting up a SAML 2.0 application in Okta.",
                "key_points": [
                    "Single Sign-On URL (ACS URL) — where Okta POSTs the assertion.",
                    "Audience URI (SP Entity ID) — the unique identifier for the application.",
                    "Name ID Format — usually EmailAddress or Persistent.",
                    "Attribute Statements — map Okta profile attributes to SAML assertion attributes.",
                    "Download Okta Metadata XML and import into SP to complete trust setup.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "In a SAML flow, Okta plays which role?",
                "options": ["Service Provider (SP)", "Identity Provider (IdP)", "Resource Server", "Relying Party"],
                "answer": 1,
                "explanation": "Okta is the Identity Provider (IdP) in SAML. It authenticates users and issues SAML assertions to the Service Provider.",
            },
            {
                "q": "What is an ID Token in OIDC?",
                "options": [
                    "An XML document with user attributes",
                    "A JWT containing claims about the authenticated user",
                    "An opaque string used to call APIs",
                    "A long-lived token used for silent re-authentication",
                ],
                "answer": 1,
                "explanation": "An ID Token is a JWT that contains claims about who the user is (identity). An Access Token is used to call APIs.",
            },
            {
                "q": "What is the ACS URL in a SAML configuration?",
                "options": [
                    "The URL of the Okta login page",
                    "The application endpoint where Okta POSTs the SAML assertion",
                    "The unique identifier for the Service Provider",
                    "The SAML metadata download URL",
                ],
                "answer": 1,
                "explanation": "ACS (Assertion Consumer Service) URL is the SP endpoint that receives and processes the SAML assertion posted by Okta.",
            },
            {
                "q": "Which OIDC grant type should be used for a traditional server-side web application?",
                "options": ["Implicit flow", "Client Credentials", "Authorization Code flow", "Device Authorization"],
                "answer": 2,
                "explanation": "Authorization Code flow is the most secure and recommended grant type for server-side web apps, where the client secret can be kept confidential.",
            },
            {
                "q": "What is PKCE and when is it required?",
                "options": [
                    "A SAML extension for signed assertions; required for all SAML apps",
                    "A SAML binding type; required when using HTTP POST",
                    "An OAuth 2.0 extension for public clients like SPAs and mobile apps to prevent auth code interception",
                    "An Okta-specific token format; required for API access",
                ],
                "answer": 2,
                "explanation": "PKCE (Proof Key for Code Exchange) protects the Authorization Code flow for public clients (SPAs, mobile apps) that cannot store a client secret securely.",
            },
            {
                "q": "In a SAML SP-initiated flow, where does the user start?",
                "options": [
                    "At the Okta login page",
                    "At the Service Provider application",
                    "At the Okta dashboard (app tile)",
                    "At the Identity Provider metadata URL",
                ],
                "answer": 1,
                "explanation": "In SP-initiated flow, the user navigates to the application (SP), which redirects them to Okta (IdP) for authentication, then back to the SP with the assertion.",
            },
            {
                "q": "Which protocol natively supports both SSO and API authorization?",
                "options": ["SAML 2.0", "OIDC / OAuth 2.0", "LDAP", "WS-Federation"],
                "answer": 1,
                "explanation": "OIDC is built on OAuth 2.0, which provides API authorization via Access Tokens. SAML only handles authentication/SSO.",
            },
        ],
        "exam_tips": [
            "Okta = IdP for SAML; Okta = Authorization Server + IdP for OIDC.",
            "SAML assertion = XML. OIDC ID Token = JWT. Access Token = for APIs.",
            "ACS URL = where the assertion is POSTed. Audience URI = SP Entity ID.",
            "Authorization Code + PKCE is the secure modern flow for all app types.",
            "SP-initiated: user starts at app. IdP-initiated: user starts at Okta tile.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 4. Admin Roles
    # ────────────────────────────────────────────────────────────────────────
    "admin-roles": {
        "title": "Admin Roles",
        "icon": "🛡️",
        "estimated_minutes": 8,
        "summary": (
            "Okta provides built-in admin roles with predefined permissions. "
            "Understanding each role's scope — and applying the principle of least privilege — "
            "is a core exam topic and a best practice for secure Okta administration."
        ),
        "sections": [
            {
                "heading": "Built-in Admin Roles",
                "body": "Okta ships with six standard admin roles. Custom roles are available but not the focus of the Professional exam.",
                "key_points": [
                    "Super Administrator — full access to all Okta features. Can manage other admins. Assign sparingly.",
                    "Org Administrator — full access except cannot manage other Super Admins. The 'day-to-day admin' role.",
                    "App Administrator — manages specific applications (assign users, configure settings). Scoped to assigned apps.",
                    "Group Administrator — manages specific groups (add/remove members, manage group rules). Scoped to assigned groups.",
                    "Help Desk Administrator — can reset passwords and unlock users. Cannot modify policies or apps.",
                    "Read-Only Administrator — view-only access to the Okta admin console. Cannot make changes.",
                    "Report Administrator — access to reports and System Log only.",
                ],
            },
            {
                "heading": "Role Scope and Assignment",
                "body": (
                    "Roles can be assigned to individual users or to groups. "
                    "App and Group Administrators can be scoped to specific resources."
                ),
                "key_points": [
                    "Assign roles to individual users or to a group (all group members inherit the role).",
                    "App Administrator role can be scoped to specific apps — not necessarily all apps.",
                    "Group Administrator role can be scoped to specific groups.",
                    "Super Administrator roles cannot be scoped — they always apply org-wide.",
                    "Best practice: assign the least-privileged role sufficient for the task.",
                ],
            },
            {
                "heading": "Principle of Least Privilege",
                "body": (
                    "The exam frequently tests knowledge of which role to assign for a given task. "
                    "Always choose the most limited role that satisfies the requirement."
                ),
                "key_points": [
                    "Help Desk: only needs to unlock users and reset passwords — do not give Org Admin.",
                    "App Admin: only needs to manage one or two apps — do not give Org Admin.",
                    "Read-Only: auditors or reviewers who should not make changes.",
                    "Super Admin: reserved for break-glass accounts and Okta configuration tasks.",
                    "Custom roles (OIE): allow fine-grained permission sets beyond built-in roles.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "Which admin role can reset passwords and unlock user accounts but cannot modify sign-on policies?",
                "options": ["Org Administrator", "App Administrator", "Help Desk Administrator", "Read-Only Administrator"],
                "answer": 2,
                "explanation": "Help Desk Administrator is specifically designed for user support tasks: resetting passwords and unlocking accounts. It cannot change policies or app configurations.",
            },
            {
                "q": "An admin needs to manage group membership for a specific department group only. Which role should they receive?",
                "options": ["Super Administrator", "Group Administrator (scoped to that group)", "Org Administrator", "App Administrator"],
                "answer": 1,
                "explanation": "Group Administrator can be scoped to specific groups, giving the admin control over that group without org-wide access.",
            },
            {
                "q": "Which Okta admin role has full access to all features AND can manage other Super Admins?",
                "options": ["Org Administrator", "Super Administrator", "App Administrator", "Report Administrator"],
                "answer": 1,
                "explanation": "Super Administrator is the highest-privilege role with unrestricted access, including the ability to assign and remove other Super Admin roles.",
            },
            {
                "q": "An auditor needs to review the Okta configuration and system logs without making changes. Which role is most appropriate?",
                "options": ["Org Administrator", "Help Desk Administrator", "Report Administrator", "Read-Only Administrator"],
                "answer": 3,
                "explanation": "Read-Only Administrator provides view-only access to the admin console without the ability to make any changes.",
            },
            {
                "q": "Which built-in Okta admin role is most appropriate for a day-to-day Okta administrator who needs broad access but should not manage Super Admins?",
                "options": ["Super Administrator", "Org Administrator", "App Administrator", "Group Administrator"],
                "answer": 1,
                "explanation": "Org Administrator has broad access to manage users, groups, and applications but cannot modify other Super Admin assignments.",
            },
        ],
        "exam_tips": [
            "6 built-in roles: Super Admin, Org Admin, App Admin, Group Admin, Help Desk Admin, Read-Only Admin.",
            "Help Desk = reset passwords + unlock only. Cannot touch policies.",
            "App Admin and Group Admin can be scoped to specific apps/groups.",
            "Super Admin is the only role that can manage other Super Admins.",
            "Least privilege: match the role to the minimum access required for the task.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 5. Group Types and Group Rules
    # ────────────────────────────────────────────────────────────────────────
    "group-types": {
        "title": "Group Types and Group Rules",
        "icon": "👥",
        "estimated_minutes": 8,
        "summary": (
            "Okta supports three types of groups, each with different management characteristics. "
            "Group Rules enable dynamic, attribute-driven group membership — a critical tool "
            "for automating access provisioning at scale."
        ),
        "sections": [
            {
                "heading": "The Three Group Types",
                "body": "Each group type has a distinct origin and management model.",
                "key_points": [
                    "Okta Groups — created and managed directly in Okta. Membership is manual or rule-driven.",
                    "App Groups (Pushed Groups) — mastered in a downstream app (e.g., Active Directory). Pushed to Okta via provisioning.",
                    "Directory Groups — imported from an external directory (e.g., AD or LDAP). Read-only in Okta.",
                ],
            },
            {
                "heading": "Group Rules (Dynamic Groups)",
                "body": (
                    "Group Rules evaluate user profile attributes to automatically assign users to Okta Groups. "
                    "Rules are evaluated continuously and update membership as attributes change."
                ),
                "key_points": [
                    "Rules use Okta Expression Language to define conditions (e.g., user.department == 'Engineering').",
                    "Rules only apply to Okta Groups — you cannot use rules to manage AD/LDAP groups.",
                    "A rule can assign users to multiple groups simultaneously.",
                    "Excluded users: specific users can be excluded from a rule's effect.",
                    "Rules are re-evaluated when a user's profile attributes change.",
                    "Status: rules can be Active or Inactive. Only Active rules affect membership.",
                ],
            },
            {
                "heading": "Group Rule Expression Language",
                "body": "Okta Expression Language (OEL) is used to write rule conditions.",
                "key_points": [
                    "String match: user.department == 'Sales'",
                    "Contains: user.email.endsWith('@company.com')",
                    "AND/OR: user.department == 'Sales' AND user.status == 'ACTIVE'",
                    "Group membership check: isMemberOfGroup('00g...')",
                    "Null check: user.manager != null",
                ],
            },
            {
                "heading": "Using Groups for Access Control",
                "body": "Groups are the primary mechanism for assigning app access and policies in Okta.",
                "key_points": [
                    "Assign apps to groups rather than individual users — scales better.",
                    "Password policies are scoped to groups.",
                    "Group membership drives SCIM provisioning to downstream apps.",
                    "Groups can be used as conditions in sign-on policy rules.",
                    "Everyone group: all users belong to this group; cannot be removed.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "Which group type in Okta is managed directly in Okta and supports Group Rules for dynamic membership?",
                "options": ["App Group", "Directory Group", "Okta Group", "AD Group"],
                "answer": 2,
                "explanation": "Group Rules only apply to Okta Groups (not app or directory groups). Okta Groups can have members assigned manually or dynamically via rules.",
            },
            {
                "q": "A group rule uses the expression: user.department == 'Finance'. When is this rule re-evaluated for a user?",
                "options": [
                    "Only when an admin manually triggers a re-evaluation",
                    "Every 24 hours on a scheduled basis",
                    "When the user's profile attributes change",
                    "At each user login",
                ],
                "answer": 2,
                "explanation": "Group rules are re-evaluated when a user's profile attributes change, ensuring dynamic membership stays current.",
            },
            {
                "q": "Which of the following is a valid Okta Expression Language condition for a group rule?",
                "options": [
                    "user.department LIKE 'Eng%'",
                    "user.department == 'Engineering'",
                    "department = 'Engineering'",
                    "SELECT * WHERE department='Engineering'",
                ],
                "answer": 1,
                "explanation": "Okta Expression Language uses == for equality. The correct syntax is user.department == 'Engineering'.",
            },
            {
                "q": "A company imports groups from Active Directory into Okta. What type are these groups?",
                "options": ["Okta Groups", "App Groups", "Directory Groups", "Dynamic Groups"],
                "answer": 2,
                "explanation": "Groups imported from Active Directory or LDAP are Directory Groups. They are read-only in Okta and mastered in the external directory.",
            },
            {
                "q": "Which Okta group contains ALL users in the org and cannot have members removed from it?",
                "options": ["Default Group", "Everyone Group", "Org Group", "Universal Group"],
                "answer": 1,
                "explanation": "The 'Everyone' group automatically includes all users in the Okta org. You cannot remove users from this group.",
            },
        ],
        "exam_tips": [
            "3 group types: Okta Groups (manageable), App Groups (pushed from apps), Directory Groups (imported, read-only).",
            "Group Rules = dynamic membership based on user attributes. Only works on Okta Groups.",
            "Expression Language: user.attribute == 'value' — double equals, dot notation.",
            "Everyone group: all users, cannot remove members.",
            "Assign apps to groups, not individuals — scales better and aligns with policy enforcement.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 6. Universal Directory / Profile Mastering
    # ────────────────────────────────────────────────────────────────────────
    "universal-directory": {
        "title": "Universal Directory & Profile Mastering",
        "icon": "🗂️",
        "estimated_minutes": 10,
        "summary": (
            "Okta's Universal Directory (UD) is the central user store that aggregates identity data "
            "from multiple sources. Profile Mastering defines which source of truth controls each "
            "user attribute — critical for consistent identity data across the enterprise."
        ),
        "sections": [
            {
                "heading": "Universal Directory Overview",
                "body": (
                    "The Universal Directory is Okta's built-in identity store. "
                    "It holds a unified user profile for every identity — regardless of where they originate."
                ),
                "key_points": [
                    "Stores user profiles from Okta, Active Directory, LDAP, HR systems, and other sources.",
                    "Every user has a single unified Okta user profile in the UD.",
                    "Custom attributes can be added to the UD profile schema.",
                    "Profile attributes can be mapped to and from applications.",
                    "Okta acts as the 'hub' — all identity data flows through the UD.",
                ],
            },
            {
                "heading": "Profile Sources (Mastering)",
                "body": (
                    "A Profile Source is an identity provider that has the authority to write specific "
                    "attributes to the Okta user profile. Mastering determines the source of truth."
                ),
                "key_points": [
                    "Profile Source: the app or directory that 'masters' (owns) a user profile or specific attributes.",
                    "When a profile source updates an attribute, Okta updates the UD profile automatically.",
                    "Common profile sources: Active Directory, LDAP, HR systems (Workday, BambooHR), Okta itself.",
                    "A user can only have ONE profile source (for the overall profile master).",
                    "Apps can be set as profile sources via provisioning — 'Import' direction.",
                ],
            },
            {
                "heading": "Attribute-Level Mastering",
                "body": (
                    "Attribute-Level Mastering allows different attributes to be controlled by different sources. "
                    "This is more granular than setting a single profile master."
                ),
                "key_points": [
                    "Individual attributes can be configured with their own mastering source.",
                    "Example: AD masters firstName and lastName; HR system masters department and costCenter.",
                    "Attribute-level mastering overrides the profile-level master for those specific attributes.",
                    "Attributes not mastered by any source can be edited by the user or an admin.",
                    "Mastered attributes appear locked in the Okta admin UI — cannot be edited manually.",
                ],
            },
            {
                "heading": "Profile Mastering Priority",
                "body": "When multiple sources could update an attribute, mastering priority determines which wins.",
                "key_points": [
                    "Priority is set in the app's provisioning settings (Okta Admin → Applications → Provisioning → To Okta).",
                    "Higher priority source wins if two sources push conflicting values.",
                    "Deactivating a user in the profile source can trigger deprovisioning in Okta.",
                    "Push Groups feature: groups mastered in an app can be pushed to Okta.",
                    "Import safety: Okta can be configured to confirm before overwriting existing values.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "What is a Profile Source in Okta's Universal Directory?",
                "options": [
                    "A backup copy of user profiles stored in the cloud",
                    "An application or directory that has authority to write attributes to the Okta user profile",
                    "A template for new user accounts",
                    "The Okta System Log entry tracking profile changes",
                ],
                "answer": 1,
                "explanation": "A Profile Source (or profile master) is the authoritative source for a user's profile data. When it updates an attribute, that change flows into the Okta UD.",
            },
            {
                "q": "A company uses Active Directory to master firstName and lastName, and Workday to master department. This is an example of:",
                "options": [
                    "Profile-level mastering",
                    "Attribute-level mastering",
                    "App group mastering",
                    "Universal mastering",
                ],
                "answer": 1,
                "explanation": "Attribute-level mastering allows different attributes to be controlled by different source systems — more granular than a single profile master.",
            },
            {
                "q": "An admin tries to manually edit a user's 'department' attribute in Okta but the field is greyed out. Why?",
                "options": [
                    "The user's account is DEPROVISIONED",
                    "The attribute is mastered by a profile source and cannot be edited manually in Okta",
                    "The admin does not have the correct role",
                    "The attribute is a read-only system attribute",
                ],
                "answer": 1,
                "explanation": "When an attribute is mastered by a profile source, Okta locks the field in the admin UI to prevent manual overrides that would be overwritten by the next sync.",
            },
            {
                "q": "How many Profile Sources (masters) can a single Okta user have for their overall profile?",
                "options": ["Unlimited", "As many as the number of connected apps", "One", "Two — one primary and one secondary"],
                "answer": 2,
                "explanation": "A user can only have ONE profile master (profile source). However, individual attributes can be attribute-level mastered by different sources.",
            },
            {
                "q": "What happens when the profile source for a user deactivates that user?",
                "options": [
                    "Nothing — Okta and the source are independent",
                    "The user's Okta account is automatically deprovisioned",
                    "The user is moved to STAGED state",
                    "The user's apps are removed but the Okta account stays ACTIVE",
                ],
                "answer": 1,
                "explanation": "When a profile source (e.g., Active Directory) deactivates a user, Okta can be configured to automatically deprovision (deactivate) the user's Okta account.",
            },
        ],
        "exam_tips": [
            "Universal Directory = central hub for all identity data in Okta.",
            "Profile Source = the system that 'owns' and writes the user profile to Okta.",
            "One profile master per user. Multiple attribute-level masters are possible.",
            "Mastered attributes are locked in the Okta UI — cannot be manually edited.",
            "Deactivating a user in the profile source can trigger automatic deprovisioning in Okta.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 7. SCIM Provisioning
    # ────────────────────────────────────────────────────────────────────────
    "scim-provisioning": {
        "title": "SCIM Provisioning",
        "icon": "🔄",
        "estimated_minutes": 10,
        "summary": (
            "SCIM (System for Cross-domain Identity Management) is an open standard for automating "
            "user lifecycle management between Okta and connected applications. "
            "Understanding push vs pull, provisioning features, and attribute mappings is essential "
            "for the Professional exam."
        ),
        "sections": [
            {
                "heading": "What is SCIM?",
                "body": (
                    "SCIM 2.0 is an API standard (RFC 7642-7644) that defines how identity data "
                    "is created, read, updated, and deleted across systems."
                ),
                "key_points": [
                    "SCIM uses REST API with JSON payloads to sync identity data.",
                    "Okta acts as the SCIM client (provisioning agent); the app acts as the SCIM server.",
                    "SCIM replaces manual CSV exports and custom scripts for user provisioning.",
                    "Supported operations: Create, Read, Update, Delete/Deactivate users and groups.",
                    "SCIM 2.0 is the current version; SCIM 1.1 is legacy but still encountered.",
                ],
            },
            {
                "heading": "Push vs Pull (Import)",
                "body": (
                    "Provisioning can flow in two directions. The direction determines whether Okta "
                    "or the app is the source of truth."
                ),
                "key_points": [
                    "Push (Okta → App): Okta creates/updates/deactivates users in the downstream app.",
                    "Pull / Import (App → Okta): Okta imports user records from the app into the UD.",
                    "Both directions can be enabled simultaneously for full lifecycle sync.",
                    "Push is the most common direction — Okta is the IdP and source of truth.",
                    "Import is used when the app (e.g., HR system) is the authoritative source.",
                ],
            },
            {
                "heading": "Provisioning Features",
                "body": "Okta exposes granular provisioning feature toggles per application.",
                "key_points": [
                    "Create Users — automatically create accounts in the app when assigned in Okta.",
                    "Update User Attributes — sync profile changes from Okta to the app.",
                    "Deactivate Users — disable the app account when the Okta user is deprovisioned or unassigned.",
                    "Sync Password — push Okta-managed passwords to the app (not needed for SSO apps).",
                    "Push Groups — sync Okta group memberships to the app as groups.",
                    "Import Users — pull user accounts from the app into Okta.",
                    "Import Groups — pull group data from the app into Okta.",
                ],
            },
            {
                "heading": "Attribute Mappings",
                "body": "Attribute mappings define how Okta profile fields correspond to app profile fields.",
                "key_points": [
                    "Configured in the app's Provisioning → To App / To Okta sections.",
                    "Direction: 'To App' maps Okta attributes to the app; 'To Okta' maps app attributes to UD.",
                    "Transformations: expressions can transform attribute values during mapping.",
                    "Required attributes must be mapped for provisioning to succeed.",
                    "Unmapped attributes are not synced — gaps can cause provisioning errors.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "In Okta SCIM provisioning, which system acts as the SCIM client?",
                "options": ["The downstream application (SCIM server)", "Okta", "Active Directory", "The SCIM API gateway"],
                "answer": 1,
                "explanation": "Okta is the SCIM client — it initiates provisioning requests to the app, which acts as the SCIM server.",
            },
            {
                "q": "Which SCIM provisioning feature automatically disables a user's app account when they are deprovisioned in Okta?",
                "options": ["Create Users", "Sync Password", "Deactivate Users", "Import Users"],
                "answer": 2,
                "explanation": "'Deactivate Users' triggers app account deactivation when the user is deprovisioned in Okta or removed from the app assignment.",
            },
            {
                "q": "An HR system is the source of truth for employee data. Okta needs to import users from the HR system. Which SCIM direction is this?",
                "options": ["Push (Okta → App)", "Pull / Import (App → Okta)", "Bi-directional sync", "Group Push"],
                "answer": 1,
                "explanation": "Import / Pull direction flows from the app (HR system) into Okta. The app is the source of truth for user data.",
            },
            {
                "q": "What is the purpose of 'Push Groups' in Okta SCIM provisioning?",
                "options": [
                    "Import group data from an app into Okta",
                    "Sync Okta group memberships to the downstream application",
                    "Create new Okta groups from SCIM attributes",
                    "Allow users to self-enrol in groups",
                ],
                "answer": 1,
                "explanation": "'Push Groups' syncs Okta group memberships to the downstream app, so the app reflects the same groups as Okta.",
            },
            {
                "q": "Where are attribute mappings for SCIM provisioning configured in Okta?",
                "options": [
                    "Universal Directory → Profile Editor",
                    "The application's Provisioning tab → To App / To Okta sections",
                    "Security → API → Token Management",
                    "Directory → Profile Sources",
                ],
                "answer": 1,
                "explanation": "Attribute mappings are configured in the application's Provisioning tab. 'To App' maps Okta attributes to the app; 'To Okta' maps app attributes back to Okta.",
            },
        ],
        "exam_tips": [
            "SCIM = REST API standard for automating user lifecycle. Okta is the SCIM client.",
            "Push = Okta → App (most common). Import = App → Okta.",
            "6 provisioning features: Create, Update Attributes, Deactivate, Sync Password, Push Groups, Import.",
            "Deactivate Users = auto-disable in app when unassigned or deprovisioned in Okta.",
            "Attribute mappings: 'To App' direction is for push; 'To Okta' is for import.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 8. ThreatInsight
    # ────────────────────────────────────────────────────────────────────────
    "threat-insight": {
        "title": "ThreatInsight Modes",
        "icon": "🔍",
        "estimated_minutes": 6,
        "summary": (
            "ThreatInsight is Okta's built-in threat detection service that uses "
            "machine learning and threat intelligence to identify and respond to "
            "suspicious authentication behaviour. It operates in two modes and "
            "integrates with sign-on policy rules."
        ),
        "sections": [
            {
                "heading": "ThreatInsight Overview",
                "body": (
                    "ThreatInsight analyses authentication requests in real time, "
                    "scoring IPs and requests for risk. It aggregates signals across all Okta tenants."
                ),
                "key_points": [
                    "Uses ML models trained on authentication data across the Okta network.",
                    "Identifies credential stuffing, password spraying, and anomalous login patterns.",
                    "Risk signals include IP reputation, geolocation anomalies, and bot-like behaviour.",
                    "Enabled in Security → General → ThreatInsight in the admin console.",
                    "ThreatInsight events are logged in the System Log (event type: security.threat.detected).",
                ],
            },
            {
                "heading": "Operating Modes",
                "body": "ThreatInsight operates in one of two modes. The mode determines whether suspicious IPs are blocked.",
                "key_points": [
                    "Audit Mode (Log Only) — suspicious activity is logged but not blocked. Users can still authenticate.",
                    "Block Mode (Log and Enforce) — requests from high-risk IPs are actively blocked. Users cannot authenticate from those IPs.",
                    "Audit mode is safe to enable first; review logs before switching to Block mode.",
                    "Block mode provides active protection but may cause false positives for legitimate users on shared IPs.",
                ],
            },
            {
                "heading": "IP Exemptions",
                "body": "Trusted IPs can be exempted from ThreatInsight evaluation to prevent false positives.",
                "key_points": [
                    "Add trusted IP ranges to the ThreatInsight exemption list.",
                    "Exempted IPs bypass ThreatInsight risk scoring but still go through sign-on policy evaluation.",
                    "Use exemptions for corporate office IP ranges or known VPN egress IPs.",
                    "Network Zones can also be used in sign-on policy to differentiate trusted vs untrusted networks.",
                ],
            },
            {
                "heading": "ThreatInsight and Sign-On Policy Integration",
                "body": "ThreatInsight risk signals can be used as conditions in sign-on policy rules.",
                "key_points": [
                    "Policy rules can reference ThreatInsight risk level: any risk, medium risk, high risk.",
                    "Example rule: if ThreatInsight detects high risk → deny access.",
                    "Example rule: if ThreatInsight detects medium risk → require MFA.",
                    "Combining ThreatInsight with MFA requirements creates adaptive authentication.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "In ThreatInsight Audit Mode, what happens when a suspicious IP is detected?",
                "options": [
                    "The user is blocked from authenticating",
                    "The event is logged but the user can still authenticate",
                    "The user is prompted for MFA",
                    "The account is locked out",
                ],
                "answer": 1,
                "explanation": "Audit Mode (Log Only) records suspicious activity in the System Log but does not block the authentication attempt.",
            },
            {
                "q": "Which ThreatInsight mode actively blocks authentication attempts from high-risk IPs?",
                "options": ["Audit Mode", "Monitor Mode", "Block Mode", "Enforce Mode"],
                "answer": 2,
                "explanation": "Block Mode (Log and Enforce) actively prevents authentication from IPs identified as high-risk by ThreatInsight.",
            },
            {
                "q": "A company's corporate VPN egress IP is being incorrectly flagged by ThreatInsight. What is the recommended solution?",
                "options": [
                    "Disable ThreatInsight entirely",
                    "Switch to Audit Mode permanently",
                    "Add the VPN IP to the ThreatInsight IP exemption list",
                    "Create a new Okta org for corporate users",
                ],
                "answer": 2,
                "explanation": "Adding trusted IPs to the ThreatInsight exemption list prevents those IPs from being evaluated, eliminating false positives for known corporate IPs.",
            },
            {
                "q": "Where can ThreatInsight detected events be reviewed?",
                "options": ["Application dashboard", "Okta System Log", "User profile page", "Active Directory audit log"],
                "answer": 1,
                "explanation": "ThreatInsight events are recorded in the Okta System Log with event type security.threat.detected.",
            },
        ],
        "exam_tips": [
            "Two modes: Audit (log only, no block) and Block (log + enforce, blocks high-risk IPs).",
            "Start with Audit mode — review logs before enabling Block mode.",
            "Exemptions: add trusted IPs to bypass ThreatInsight risk scoring.",
            "ThreatInsight integrates with sign-on policy: use risk level as a rule condition.",
            "Events appear in System Log under security.threat.detected.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 9. Passwordless / Phishing-Resistant Factors
    # ────────────────────────────────────────────────────────────────────────
    "passwordless-factors": {
        "title": "Passwordless & Phishing-Resistant Factors",
        "icon": "🔐",
        "estimated_minutes": 10,
        "summary": (
            "Passwordless authentication eliminates the password from the login flow, "
            "reducing phishing risk and improving UX. Phishing-resistant factors cryptographically "
            "bind authentication to the origin, making credential theft attacks ineffective."
        ),
        "sections": [
            {
                "heading": "Passwordless Authentication",
                "body": (
                    "Passwordless means users authenticate without a password — using a factor "
                    "that proves possession and/or biometrics instead."
                ),
                "key_points": [
                    "Okta FastPass — Okta's native passwordless authenticator. Uses device-bound keys + biometrics.",
                    "FIDO2 / WebAuthn — W3C standard for hardware security keys (YubiKey) and platform authenticators (Face ID, Touch ID).",
                    "Magic Link / Email — one-time link sent to email; lower assurance but passwordless.",
                    "Push notification — Okta Verify push; user approves on phone (not phishing-resistant).",
                    "Passwordless ≠ phishing-resistant. Some passwordless factors can still be phished.",
                ],
            },
            {
                "heading": "Phishing-Resistant Factors",
                "body": (
                    "Phishing-resistant factors use public-key cryptography where the private key "
                    "never leaves the device and the credential is bound to the origin (domain). "
                    "Even if a user is tricked onto a fake site, the credential cannot be used."
                ),
                "key_points": [
                    "FIDO2 / WebAuthn security keys — hardware keys (YubiKey, Titan). Keys are site-bound.",
                    "FIDO2 platform authenticators — built-in authenticators (Windows Hello, Face ID, Touch ID).",
                    "Okta FastPass — uses device-bound keys; resistant to phishing when used with biometrics.",
                    "Phishing-resistant = credential is cryptographically bound to the relying party origin.",
                    "SMS OTP, TOTP (Google Authenticator), push notifications are NOT phishing-resistant.",
                ],
            },
            {
                "heading": "Okta FastPass",
                "body": (
                    "Okta FastPass is Okta's proprietary passwordless authenticator available via Okta Verify. "
                    "It supports both passwordless and MFA scenarios."
                ),
                "key_points": [
                    "Available on iOS, Android, macOS, and Windows via the Okta Verify app.",
                    "Uses device-bound cryptographic keys — private key never leaves the device.",
                    "Can require biometric verification for highest assurance.",
                    "Works with OIE Authentication Policies using the 'possession' and 'biometric' factors.",
                    "Requires Okta Identity Engine (OIE) — not available in Classic Okta.",
                    "Device must be registered (enrolled) before FastPass can be used.",
                ],
            },
            {
                "heading": "Configuring Phishing-Resistant Policy (OIE)",
                "body": (
                    "In OIE, Authentication Policy rules can require phishing-resistant authenticators "
                    "using the Authenticator Assurance concept."
                ),
                "key_points": [
                    "Policy rule action: 'Required' authenticator constraint — set to 'Phishing Resistant'.",
                    "Only FIDO2 and Okta FastPass (with biometric) satisfy phishing-resistant requirement.",
                    "SMS, TOTP, and email do NOT satisfy phishing-resistant policy requirements.",
                    "Phishing-resistant policies are recommended for admin access and high-value apps.",
                    "Combine with device trust for defence-in-depth: phishing-resistant + managed device.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "Which of the following factors is considered phishing-resistant?",
                "options": [
                    "SMS one-time passcode",
                    "TOTP (Google Authenticator)",
                    "FIDO2 / WebAuthn security key",
                    "Email magic link",
                ],
                "answer": 2,
                "explanation": "FIDO2/WebAuthn security keys are phishing-resistant because the credential is cryptographically bound to the origin. Even if a user is tricked, the key won't work on a fake site.",
            },
            {
                "q": "What makes a factor 'phishing-resistant'?",
                "options": [
                    "It requires a biometric scan",
                    "The credential is cryptographically bound to the relying party origin",
                    "It uses a one-time passcode",
                    "It requires a hardware device",
                ],
                "answer": 1,
                "explanation": "Phishing-resistant factors use public-key cryptography where the credential is bound to the specific site (origin). Credentials cannot be replayed on a different (fake) site.",
            },
            {
                "q": "Okta FastPass is available on which Okta platform version?",
                "options": [
                    "Classic Okta only",
                    "Both Classic Okta and OIE",
                    "Okta Identity Engine (OIE) only",
                    "Only on Okta's enterprise tier",
                ],
                "answer": 2,
                "explanation": "Okta FastPass requires Okta Identity Engine (OIE). It is not available on Classic Okta.",
            },
            {
                "q": "Which of the following is an example of a passwordless but NOT phishing-resistant factor?",
                "options": [
                    "YubiKey (FIDO2 hardware key)",
                    "Okta FastPass with biometric",
                    "Okta Verify push notification",
                    "Windows Hello (FIDO2 platform authenticator)",
                ],
                "answer": 2,
                "explanation": "Okta Verify push notification is passwordless (no password required) but is NOT phishing-resistant — an attacker could proxy the push approval.",
            },
            {
                "q": "In an OIE Authentication Policy, which authenticator satisfies a 'Phishing Resistant' constraint?",
                "options": ["Email OTP", "SMS OTP", "Google Authenticator (TOTP)", "FIDO2 WebAuthn"],
                "answer": 3,
                "explanation": "Only FIDO2 WebAuthn and Okta FastPass (with biometric) satisfy a phishing-resistant authenticator constraint in OIE policies.",
            },
        ],
        "exam_tips": [
            "Phishing-resistant = cryptographically origin-bound. FIDO2/WebAuthn, Okta FastPass (with biometric).",
            "Passwordless ≠ phishing-resistant. Push notifications are passwordless but NOT phishing-resistant.",
            "SMS, TOTP, email OTP = NOT phishing-resistant.",
            "Okta FastPass requires OIE + Okta Verify app + device enrollment.",
            "Policy rule: set authenticator constraint to 'Phishing Resistant' to require FIDO2/FastPass.",
        ],
    },

    # ────────────────────────────────────────────────────────────────────────
    # 10. System Log
    # ────────────────────────────────────────────────────────────────────────
    "system-log": {
        "title": "System Log",
        "icon": "📜",
        "estimated_minutes": 8,
        "summary": (
            "The Okta System Log is the authoritative audit trail for all events in your Okta org. "
            "Understanding event types, the actor/target model, query syntax, "
            "and retention policies is essential for security investigations and compliance."
        ),
        "sections": [
            {
                "heading": "System Log Overview",
                "body": (
                    "The System Log records all admin actions, user authentications, policy evaluations, "
                    "and provisioning events. It is the first place to investigate security incidents."
                ),
                "key_points": [
                    "Accessible at Admin Console → Reports → System Log.",
                    "Events are immutable — cannot be edited or deleted.",
                    "Real-time: events typically appear within seconds of occurring.",
                    "Exportable via the System Log API (paginated, filter-able).",
                    "Retention: 90 days by default (longer retention requires log streaming).",
                ],
            },
            {
                "heading": "Event Structure",
                "body": "Each System Log event follows a consistent JSON structure with key fields.",
                "key_points": [
                    "eventType — the type of event (e.g., user.session.start, policy.evaluate).",
                    "actor — who performed the action (user, admin, system). Includes displayName, id, type.",
                    "target — the object(s) affected (user, group, app, policy). Array of targets.",
                    "outcome — result of the action (SUCCESS, FAILURE, SKIPPED, ALLOW, DENY).",
                    "client — browser/device info, IP address, geolocation.",
                    "request — HTTP request details.",
                    "displayMessage — human-readable description of the event.",
                ],
            },
            {
                "heading": "Common Event Types",
                "body": "Key event types to recognise for the exam.",
                "key_points": [
                    "user.session.start — user successfully authenticated to Okta.",
                    "user.session.end — user signed out.",
                    "user.authentication.auth_via_mfa — MFA authentication completed.",
                    "user.account.lock — user account was locked out.",
                    "user.account.reset_password — password was reset.",
                    "user.lifecycle.activate — user was activated.",
                    "user.lifecycle.deactivate — user was deprovisioned/deactivated.",
                    "policy.evaluate_sign_on — sign-on policy was evaluated.",
                    "security.threat.detected — ThreatInsight detected a threat.",
                    "application.provision.user — SCIM provisioning event for a user.",
                ],
            },
            {
                "heading": "Querying the System Log",
                "body": "The System Log UI and API support SCIM filter syntax for querying events.",
                "key_points": [
                    "Filter by event type: eventType eq \"user.session.start\"",
                    "Filter by actor: actor.id eq \"00u...\"",
                    "Filter by target: target.id eq \"00u...\"",
                    "Filter by outcome: outcome.result eq \"FAILURE\"",
                    "Date range: published gt \"2024-01-01T00:00:00Z\"",
                    "Full-text search available in the admin UI — less precise than API filters.",
                    "API endpoint: GET /api/v1/logs with query parameters.",
                ],
            },
            {
                "heading": "Log Streaming and Retention",
                "body": "For longer retention and real-time alerting, stream logs to an external SIEM.",
                "key_points": [
                    "Default retention: 90 days in the Okta UI.",
                    "Log Streaming: push events to AWS EventBridge or Splunk in real time.",
                    "Log Streaming is configured at Security → Log Streaming in the admin console.",
                    "Third-party SIEMs (Splunk, Microsoft Sentinel) can ingest via API polling or streaming.",
                    "For compliance (SOC 2, ISO 27001), streaming + long-term storage is required.",
                ],
            },
        ],
        "quiz_questions": [
            {
                "q": "What is the default System Log retention period in Okta?",
                "options": ["30 days", "60 days", "90 days", "1 year"],
                "answer": 2,
                "explanation": "Okta retains System Log events for 90 days by default. Log streaming to an external system is needed for longer retention.",
            },
            {
                "q": "In a System Log event, which field identifies who performed the action?",
                "options": ["target", "outcome", "actor", "client"],
                "answer": 2,
                "explanation": "The 'actor' field identifies who performed the action — this could be a user, admin, or system process.",
            },
            {
                "q": "Which System Log event type indicates a user successfully authenticated to Okta?",
                "options": [
                    "user.lifecycle.activate",
                    "user.session.start",
                    "user.authentication.auth_via_mfa",
                    "policy.evaluate_sign_on",
                ],
                "answer": 1,
                "explanation": "user.session.start is logged when a user successfully completes authentication and starts an Okta session.",
            },
            {
                "q": "A security team needs System Log events retained for 1 year for compliance. What should they configure?",
                "options": [
                    "Increase the Okta log retention setting to 1 year",
                    "Configure Log Streaming to an external system like Splunk",
                    "Download logs monthly and store in S3",
                    "Enable ThreatInsight to extend log retention",
                ],
                "answer": 1,
                "explanation": "Log Streaming sends events in real time to an external system (e.g., Splunk, AWS EventBridge) for long-term retention beyond Okta's 90-day default.",
            },
            {
                "q": "Which query filter finds all failed authentication events in the System Log API?",
                "options": [
                    "eventType eq \"user.session.start\" AND result eq \"FAILURE\"",
                    "outcome.result eq \"FAILURE\"",
                    "status eq \"FAILURE\"",
                    "event.outcome eq \"BLOCKED\"",
                ],
                "answer": 1,
                "explanation": "The System Log API uses SCIM filter syntax. outcome.result eq \"FAILURE\" correctly filters for events where the outcome was a failure.",
            },
            {
                "q": "Where in the Okta admin console is the System Log accessed?",
                "options": [
                    "Security → ThreatInsight",
                    "Directory → People",
                    "Reports → System Log",
                    "Applications → Logs",
                ],
                "answer": 2,
                "explanation": "The System Log is located at Reports → System Log in the Okta admin console.",
            },
        ],
        "exam_tips": [
            "90-day default retention. Use Log Streaming for longer retention (compliance).",
            "Actor = who did it. Target = what was affected. Outcome = SUCCESS/FAILURE.",
            "Key events: user.session.start, user.account.lock, user.lifecycle.deactivate, security.threat.detected.",
            "API filter syntax: outcome.result eq \"FAILURE\" — use double quotes, dot notation.",
            "Log Streaming → AWS EventBridge or Splunk for real-time SIEM integration.",
        ],
    },
}
