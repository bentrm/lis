export const EN = 'en';
export const DE = 'de';
export const CS = 'cs';

/**
 * Current document language as returned by the server.
 * @type {string} language code
 */
export const currentLanguage = document.documentElement.lang;

/**
 * Returns the field name holding the localized value in the given language.
 * Defaults to the current user language.
 *
 * @param fieldName Generic name of the field.
 * @param language Language that is to be retrieved.
 * @returns {string}
 */
export const transFieldName = (fieldName, language) => {
  language = language || currentLanguage;
  if (language === EN) {
    return fieldName;
  } else if (language === DE) {
    return `${fieldName}_${DE}`;
  } else if (language === CS) {
    return `${fieldName}_${CS}`;
  }
  throw new Error("Unsupported language code: " + language)
};

/**
 * Returns the field name holding the localized value in the given language.
 * Defaults to the current user language.
 *
 * TODO: Respect default language if value is unset or empty.
 *
 * @param attrs
 * @param fieldName
 * @param language
 * @param defaultLanguage
 * @returns {*}
 */
export const trans = (attrs, fieldName, language) => {
  language = language || currentLanguage;
  return attrs[transFieldName(fieldName, language)];
};
