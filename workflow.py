# apps/wire/workflow.py

WIRE_WORKFLOW = {
    "rawmaterial": {
        "description": "Initial intake and approval of raw materials.",
        "steps": [
            {
                "step": 1,
                "actor_permission": "QC",
                "action": "Fill all fields for the raw material.",
                "details": None,
                "on_reject": None
            },
            {
                "step": 2,
                "actor_permission": "OP",
                "action": "Confirm or Reject the raw material submission.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 1
                }
            },
            {
                "step": 3,
                "actor_permission": "QC",
                "action": "Confirm or Reject the raw material submission.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 1
                }
            },
            {
                "step": 4,
                "actor_permission": "PM",
                "action": "Finalize confirmation or rejection of the raw material.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 1
                }
            }
        ]
    },
    "license": {
        "description": "Approval process for the material license.",
        "steps": [
            {
                "step": 1,
                "actor_permission": "QC",
                "action": "Fill all fields for the license.",
                "details": None,
                "on_reject": None
            },
            {
                "step": 2,
                "actor_permission": "DM",
                "action": "Confirm or Reject the license submission.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 1
                }
            },
            {
                "step": 3,
                "actor_permission": "PS",
                "action": "Confirm or Reject the license submission.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 1
                }
            },
            {
                "step": 4,
                "actor_permission": "FO",
                "action": "Finalize confirmation or rejection of the license.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 1
                }
            }
        ]
    },
    "checklist": {
        "description": "Pre-production quality control checklist and approvals.",
        "steps": [
            {
                "step": 1,
                "actor_permission": "QC",
                "action": "Fill out 'FormSpecifications'.",
                "details": {
                    "form_name": "FormSpecifications"
                },
                "on_reject": None
            },
            {
                "step": 2,
                "actor_permission": "OP",
                "action": "Fill out 'qc_tests_wire'.",
                "details": {
                    "form_name": "qc_tests_wire"
                },
                "on_reject": None
            },
            {
                "step": 3,
                "actor_permission": "QC",
                "action": "Review 'qc_tests_wire' and confirm/reject for production.",
                "details": {
                    "reviewed_form": "qc_tests_wire"
                },
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 2
                }
            },
            {
                "step": 4,
                "actor_permission": "OP",
                "action": "Confirm or Reject the pre-production checklist.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 2
                }
            },
            {
                "step": 5,
                "actor_permission": "QC",
                "action": "Confirm or Reject the pre-production checklist.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 2
                }
            },
            {
                "step": 6,
                "actor_permission": "FO",
                "action": "Finalize confirmation or rejection of the pre-production checklist.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 2
                }
            }
        ]
    },
    "production": {
        "description": "Data entry and approvals during the production phase.",
        "steps": [
            {
                "step": 1,
                "actor_permission": "QC",
                "action": "Fill out 'FormSpecifications' for production.",
                "details": {
                    "form_name": "FormSpecifications"
                },
                "on_reject": None
            },
            {
                "step": 2,
                "actor_permission": "OP",
                "action": "Fill production data fields.",
                "details": {
                    "fields": [
                        "input_spool_length",
                        "input_spool_number",
                        "output_spool_length",
                        "output_spool_number",
                        "input_tank_number",
                        "output_tank_number",
                        "input_spool_remaining_length"
                    ]
                },
                "on_reject": None
            },
            {
                "step": 3,
                "actor_permission": "QC",
                "action": "Fill out 'ProductionQCTestWire' forms.",
                "details": {
                    "form_name": "ProductionQCTestWire"
                },
                "on_reject": None
            },
            {
                "step": 4,
                "actor_permission": "QC",
                "action": "Fill out 'Production_waste' form.",
                "details": {
                    "form_name": "Production_waste"
                },
                "on_reject": None
            },
            {
                "step": 5,
                "actor_permission": "OP",
                "action": "Confirm or Reject the production data entry.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 2
                }
            },
            {
                "step": 6,
                "actor_permission": "QC",
                "action": "Confirm or Reject the production data entry.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 2
                }
            },
            {
                "step": 7,
                "actor_permission": "PM",
                "action": "Confirm or Reject the production data entry.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 2
                }
            },
            {
                "step": 8,
                "actor_permission": "PS",
                "action": "Finalize confirmation or rejection of the production data entry.",
                "details": None,
                "on_reject": {
                    "message": "Must provide a rejection description.",
                    "go_to_step": 2
                }
            }
        ]
    },
    "product": {
        "description": "Final product data entry.",
        "steps": [
            {
                "step": 1,
                "actor_permission": "QC",
                "action": "Fill all fields for the final product.",
                "details": None,
                "on_reject": None
            }
        ]
    }
}

