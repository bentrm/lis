/**
 * Translation strings
 * @type {{}}
 */
const text = {
  'Author': {de: 'Autor/in', cs: ''},
  'Authors': {de: 'Autor/innen', cs: ''},
  'Memorial': {de: 'Erinnerungsstelle', cs: ''},
  'Memorials': {de: 'Erinnerungsstellen', cs: ''},
  'Search': {de: 'Suche', cs: ''}
};

/**
 * Currently delivered language. Might be different from browser language.
 */
export const currentLanguage = () => document.documentElement.lang;

export const trans = en => {
  const lang = currentLanguage();

  if (!text.hasOwnProperty(en)) {
    console.warn('Missing translation:', en);
    return en;
  }

  if (lang !== 'en') {
    if (text[en].hasOwnProperty(lang)) {
      return text[en][lang];
    } else {
      console.warn(`Missing ${lang} translation`, en);
    }
  }

  return en;
};

export default function (value) {
  if (!value) return '';
  value = value.toString().trim();
  return trans(value);
}
