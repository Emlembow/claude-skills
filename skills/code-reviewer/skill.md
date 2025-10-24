# Code Reviewer

## Description
A comprehensive code review skill that helps Claude perform thorough, constructive code reviews following industry best practices.

## When to Use
Activate this skill when:
- User requests a code review
- Analyzing code quality
- Looking for bugs, security issues, or performance problems
- Providing feedback on code changes or pull requests

## Instructions

1. **Understand Context**: Review the code's purpose, dependencies, and surrounding context
2. **Analyze Structure**: Examine overall architecture and organization
3. **Check Best Practices**: Verify adherence to language-specific conventions and patterns
4. **Identify Issues**: Look for:
   - Bugs and logic errors
   - Security vulnerabilities
   - Performance bottlenecks
   - Code smells and anti-patterns
   - Style inconsistencies
5. **Provide Feedback**: Offer constructive, actionable suggestions
6. **Prioritize**: Categorize findings by severity (critical, important, minor)

## Requirements

- Access to the codebase or code snippet
- Understanding of the programming language
- Context about the project's requirements

## Review Checklist

### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Logic is correct and clear

### Security
- [ ] No injection vulnerabilities
- [ ] Proper authentication/authorization
- [ ] Sensitive data is protected
- [ ] Input validation is present

### Performance
- [ ] No unnecessary computations
- [ ] Efficient algorithms and data structures
- [ ] Proper resource management
- [ ] No memory leaks

### Maintainability
- [ ] Code is readable and well-organized
- [ ] Naming is clear and consistent
- [ ] Comments explain "why" not "what"
- [ ] Functions are focused and single-purpose
- [ ] DRY principle is followed

### Testing
- [ ] Code is testable
- [ ] Tests exist and are meaningful
- [ ] Test coverage is adequate

## Output Format

```markdown
## Code Review Summary

### Overview
[Brief summary of the code under review]

### Critical Issues 🔴
1. [Issue] - [Location]
   - **Problem**: [Description]
   - **Impact**: [Severity and consequences]
   - **Suggestion**: [How to fix]

### Important Issues 🟡
[Similar format]

### Minor Issues 🔵
[Similar format]

### Positive Aspects ✅
- [What's done well]

### Recommendations
[General suggestions for improvement]
```

## Error Handling

- If code is incomplete, note missing sections
- If language is unfamiliar, acknowledge limitations
- If context is missing, request necessary information
- Focus on what can be determined from available information

## Notes

- Be constructive and specific
- Explain the "why" behind suggestions
- Consider the broader context and project goals
- Balance thoroughness with practicality
- Praise good practices to reinforce positive patterns
