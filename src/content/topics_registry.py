"""
Master ordered list of Okta Professional certification topics.
The slug must match a key in okta_professional.TOPICS.
"""

TOPICS_LIST = [
    {
        "slug": "user-lifecycle",
        "title": "User Lifecycle States",
        "icon": "👤",
        "estimated_minutes": 10,
        "description": "The 7 lifecycle states and how users transition between them.",
    },
    {
        "slug": "policy-evaluation",
        "title": "Policy Evaluation Order",
        "icon": "📋",
        "estimated_minutes": 8,
        "description": "How Okta prioritises and evaluates sign-on and password policies.",
    },
    {
        "slug": "saml-vs-oidc",
        "title": "SAML vs OIDC Key Terms",
        "icon": "🔑",
        "estimated_minutes": 12,
        "description": "Assertions vs tokens, SP/IdP roles, claims, and protocol flows.",
    },
    {
        "slug": "admin-roles",
        "title": "Admin Roles",
        "icon": "🛡️",
        "estimated_minutes": 8,
        "description": "Built-in admin roles, their scope, and least-privilege design.",
    },
    {
        "slug": "group-types",
        "title": "Group Types and Group Rules",
        "icon": "👥",
        "estimated_minutes": 8,
        "description": "Okta, app, and directory groups plus dynamic group rule syntax.",
    },
    {
        "slug": "universal-directory",
        "title": "Universal Directory & Profile Mastering",
        "icon": "🗂️",
        "estimated_minutes": 10,
        "description": "Profile sources, mastering priority, and attribute-level overrides.",
    },
    {
        "slug": "scim-provisioning",
        "title": "SCIM Provisioning",
        "icon": "🔄",
        "estimated_minutes": 10,
        "description": "SCIM 2.0 push/pull, provisioning features, and attribute mappings.",
    },
    {
        "slug": "threat-insight",
        "title": "ThreatInsight Modes",
        "icon": "🔍",
        "estimated_minutes": 6,
        "description": "Audit and Block modes, IP exemptions, and System Log events.",
    },
    {
        "slug": "passwordless-factors",
        "title": "Passwordless & Phishing-Resistant Factors",
        "icon": "🔐",
        "estimated_minutes": 10,
        "description": "FIDO2/WebAuthn, Okta FastPass, biometrics, and phishing-resistant policy.",
    },
    {
        "slug": "system-log",
        "title": "System Log",
        "icon": "📜",
        "estimated_minutes": 8,
        "description": "Event types, actors, targets, query syntax, and log retention.",
    },
]
