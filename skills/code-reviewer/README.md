# Code Reviewer Skill

## Overview

The Code Reviewer skill enables Claude to perform comprehensive, professional code reviews following industry best practices. It provides structured, actionable feedback on code quality, security, performance, and maintainability.

## Purpose

This skill helps:
- Catch bugs and logic errors early
- Identify security vulnerabilities
- Improve code quality and maintainability
- Enforce best practices and coding standards
- Provide constructive, educational feedback

## Usage

### Claude Code
```bash
# The skill activates automatically when you request a code review
"Please review this code for security issues and best practices"
```

### Example Triggers
- "Review this function"
- "Can you check this code for bugs?"
- "Please do a code review of my changes"
- "Look for security issues in this implementation"

## Features

- **Multi-aspect Analysis**: Reviews functionality, security, performance, and maintainability
- **Severity Categorization**: Classifies issues as critical, important, or minor
- **Actionable Feedback**: Provides specific suggestions for improvement
- **Educational**: Explains the reasoning behind recommendations
- **Comprehensive Checklist**: Covers all major code quality aspects

## Review Categories

1. **Functionality** - Correctness and logic
2. **Security** - Vulnerabilities and data protection
3. **Performance** - Efficiency and resource usage
4. **Maintainability** - Readability and organization
5. **Testing** - Test coverage and quality

## Files

- `skill.md` - Main skill instructions
- `README.md` - This documentation

## Contributing

Suggestions for improving this skill:
- Additional review categories
- Language-specific checklists
- Integration with linting tools
- Custom review templates

## License

MIT
