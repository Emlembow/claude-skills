# Claude Skills Collection

A curated collection of custom skills for Claude AI. Skills are composable, portable extensions that enhance Claude's capabilities for specific tasks.

## What Are Skills?

Skills are folders containing instructions, scripts, and resources that Claude can load when needed. They make Claude more powerful by providing:

- **Composable** - Stack together automatically; Claude identifies and coordinates needed skills
- **Portable** - Use the same format across Claude apps, Claude Code, and API
- **Efficient** - Load only what's necessary when needed
- **Powerful** - Can include executable code for reliable task execution

Learn more: [Anthropic Skills Announcement](https://www.anthropic.com/news/skills)

## Repository Structure

```
claude-skills/
├── skills/           # Individual skill folders
│   ├── skill-name/
│   │   ├── skill.md  # Skill definition and instructions
│   │   └── ...       # Additional resources/scripts
├── templates/        # Templates for creating new skills
└── README.md
```

## Using These Skills

### In Claude Code

1. Install skills via the Claude Code interface
2. Skills from this repo can be added manually to your `.claude/skills/` directory
3. Claude will automatically detect and use relevant skills when needed

### In Claude Apps (Pro, Max, Team, Enterprise)

1. Custom skills can be imported through the Claude interface
2. Follow the [Claude user guide](https://support.anthropic.com/) for detailed instructions

### Via API

Use the `/v1/skills` endpoint to add skills to your API requests. See [API documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for details.

## Available Skills

<!-- Add your skills here as you create them -->

*No custom skills added yet. Check back soon!*

## Creating Your Own Skills

### Quick Start

1. Copy the template from `templates/skill-template/`
2. Customize the `skill.md` file with your instructions
3. Add any necessary scripts or resources
4. Test with Claude Code or Claude apps
5. (Optional) Submit a PR to share with the community

### Skill Structure

Each skill folder should contain:

- `skill.md` - Main skill definition with instructions for Claude
- `README.md` (optional) - Human-readable documentation
- Scripts/resources (optional) - Any code or files the skill needs

### Best Practices

- **Clear instructions**: Write precise, actionable instructions for Claude
- **Scope**: Keep skills focused on specific tasks
- **Examples**: Include examples of when/how to use the skill
- **Testing**: Test thoroughly before sharing
- **Documentation**: Document dependencies and requirements
- **Modularity**: Design skills to work independently or compose with others

## Contributing

Contributions are welcome! To add a skill:

1. Fork this repository
2. Create a new skill folder under `skills/`
3. Follow the structure and best practices above
4. Submit a pull request with a description of your skill

## Resources

- [Anthropic Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Official Anthropic Skills Examples](https://github.com/anthropics/skills)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)

## License

MIT License - feel free to use and modify these skills for your needs.

---

**Note**: This is a personal collection of skills. For official Anthropic skills, visit [github.com/anthropics/skills](https://github.com/anthropics/skills).
