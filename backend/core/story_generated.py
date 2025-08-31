from .core.config import settings
from sqlalchemy.orm import session

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from model.story import storyNode , story
from .core.prompt import STORY_PROMPT


class StoryGenerator()

@classmethod:
def __get_llm(cls):
    return ChatOpenAI(
        model="gpt-4o-turbo"
    )
    




@classmethod:
def generate_story(cls , db: session , session_id: str , theme: str = "fantasy") -> story:
    llm = cls.__get_llm()
    story_parser = PydanticOutputParser(pydantic_objects=StoryLLMResponse)

    # pass the prompt 

    prompt = PromptTemplate.from_message([
        (
            "system" , 
            STORY_PROMPT
        ) , 
        (
            "user" , 
            "Generate a story with the following theme: {theme}" 
        )
    ]).partial(format_instructions = story_parser.get_format_instructions())


    raw_response = llm().invoke(prompt.invoke({}))

    response_text = raw_response

    if hasattr(raw_response, "content"):
        response_text = raw_response.content


    story_structure = story_parser.parse(response_text)

    story_db = Story(
        title = story.structure.title
        session_id = session_id
    )   

    db.add(story_db)
    db.flush() 



    root_node_data = story_structure.rootNode

    if isinstance(root_node_data, dict):
        root_node_data = StoryNodeLLM.model_validate(root_node_data)


    return story_db


    

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            options=[]
        )
        db.add(node)
        db.flush()



        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node