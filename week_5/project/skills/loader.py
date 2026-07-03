import os
import yaml


SKILLS_DIR = os.path.join(
    os.path.dirname(__file__)
)


def parse_skill(skill_file):
    """
    Parse one SKILL.md file.

    Returns:
        {
            "name": ...,
            "description": ...,
            "path": ...,
            "skill_file": ...,
            "resources": [...]
        }

    or None if the file is invalid.
    """

    with open(
        skill_file,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    if not text.startswith("---"):
        return None

    try:

        _, frontmatter, body = text.split(
            "---",
            2
        )

    except ValueError:

        return None

    metadata = yaml.safe_load(
        frontmatter
    )

    skill_dir = os.path.dirname(
        skill_file
    )

    resources = []

    for root, _, files in os.walk(
        skill_dir
    ):

        for file in files:

            if file == "SKILL.md":
                continue

            resources.append(
                os.path.relpath(
                    os.path.join(
                        root,
                        file
                    ),
                    skill_dir
                )
            )

    return {
        "name":
            metadata.get("name"),
        "description":
            metadata.get(
                "description",
                ""
            ),
        "path":
            skill_dir,
        "skill_file":
            skill_file,
        "resources":
            resources,
    }


def load_all_skills():
    """
    Scan the skills directory and return
    metadata for every valid skill.
    """

    skills = []

    for entry in os.listdir(
        SKILLS_DIR
    ):

        skill_dir = os.path.join(
            SKILLS_DIR,
            entry
        )

        if not os.path.isdir(
            skill_dir
        ):
            continue

        skill_file = os.path.join(
            skill_dir,
            "SKILL.md"
        )

        if not os.path.exists(
            skill_file
        ):
            continue

        skill = parse_skill(
            skill_file
        )

        if skill is not None:
            skills.append(skill)

    return skills
