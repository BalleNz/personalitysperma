from src.core.prompts.traits.traits_core import GET_SOCIAL_PROFILE, GET_BEHAVIORAL_PROFILE, GET_COGNITIVE_PROFILE, \
    GET_EMOTIONAL_PROFILE
from src.core.prompts.traits.traits_humor import GET_HUMOR_PROFILE
from src.core.schemas.traits.traits_basic import SocialProfileSchema, BehavioralProfileSchema, CognitiveProfileSchema, \
    EmotionalProfileSchema
from src.core.schemas.traits.traits_humor import HumorProfileSchema

GET_PROMPT_BY_SCHEMA_TYPE = {
    # [ traits ]
    SocialProfileSchema: GET_SOCIAL_PROFILE,
    BehavioralProfileSchema: GET_BEHAVIORAL_PROFILE,
    CognitiveProfileSchema: GET_COGNITIVE_PROFILE,
    EmotionalProfileSchema: GET_EMOTIONAL_PROFILE,

    # [ dark / humor ]
    HumorProfileSchema: GET_HUMOR_PROFILE

    # [ clinical ]

    # [ personality types ]
}
