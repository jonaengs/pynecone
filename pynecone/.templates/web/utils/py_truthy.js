
/**
 * Coerces the value to a boolean using similar coercion rules as Python.
 * The main difference between Javascript and Python's coercion rules
 * is in empty lists evaluate to False in Python while they
 * evaluate to True in Javascript.
 * @param val The value to coerce
 * @returns The value coerced to a boolean.
 */
export const py_truthy = (val) => {
    return Array.isArray(val) ? val.length > 0 : !!val
}
