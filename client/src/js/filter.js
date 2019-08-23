import Tagify from '@yaireo/tagify';
import {trans} from './lang';

export function bindFilterInput(element, whitelist, callback) {
  return new Tagify(element, {
    dropdown: {
      enabled: 0,
      classname: "filter-suggestion-list"
    },
    enforceWhitelist: true,
    readonly: true,
    whitelist,
  });
}

export const toFilterTags = tags => tags.map(tag => {
  const {pk} = tag;
  return {
    pk,
    value: trans(tag, 'title'),
    searchBy: Object.values(tag).join(', '),
  };
});

export const toPKs = tags => tags.map(x => x.pk);
