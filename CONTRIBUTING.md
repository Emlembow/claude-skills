# Contributing to Claude Skills Collection

Thank you for your interest in contributing! This document provides guidelines for adding skills to this collection.

## How to Contribute

### Adding a New Skill

1. **Fork the Repository**
   ```bash
   git clone https://github.com/Emlembow/claude-skills.git
   cd claude-skills
   ```

2. **Create a New Skill Folder**
   ```bash
   mkdir -p skills/your-skill-name
   cd skills/your-skill-name
   ```

3. **Use the Template**
   - Copy `templates/skill-template/skill.md` to your skill folder
   - Copy `templates/skill-template/README.md` if you want human-readable docs
   - Customize both files for your skill

4. **Follow Best Practices**
   - Keep skills focused on specific tasks
   - Write clear, actionable instructions
   - Include examples of usage
   - Test thoroughly before submitting
   - Document any dependencies

5. **Update Main README**
   - Add your skill to the "Available Skills" section
   - Include a brief description and link to the skill folder

6. **Submit a Pull Request**
   - Create a descriptive PR title (e.g., "Add [skill-name] skill")
   - Describe what the skill does and why it's useful
   - Include testing results or examples

## Skill Quality Guidelines

### Required Elements

Every skill must have:
- [ ] Clear description of purpose
- [ ] When to use / trigger conditions
- [ ] Step-by-step instructions
- [ ] At least one example
- [ ] Error handling guidance

### Optional but Recommended
- [ ] README.md for human readers
- [ ] Additional resources or scripts
- [ ] Links to related documentation
- [ ] Testing instructions

### Writing Guidelines

**Do:**
- Write precise, actionable instructions
- Use clear, simple language
- Include concrete examples
- Explain the reasoning behind approaches
- Document edge cases and limitations

**Don't:**
- Make instructions vague or ambiguous
- Assume context that isn't provided
- Skip error handling
- Forget to test the skill
- Overlook dependencies

## Code of Conduct

- Be respectful and constructive
- Focus on helping the community
- Accept feedback graciously
- Give credit where due

## Questions?

Feel free to open an issue if you have questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
