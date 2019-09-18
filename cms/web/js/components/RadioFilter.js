const template = `
  <div class="form-group">
    <label :for="id">
      {{ label }}
    </label>
    <div v-for="(option, index) in options" class="form-check">
      <input
        class="form-check-input"
        type="radio"
        :name="id"
        :id="id + '-' + index"
        :value="option.value"
        :checked="option.checked"
        v-on:change="onChange"
      >
      <label
        class="form-check-label"
        :for="id + '-' + index"
      >
        {{ option.label }}
      </label>
    </div>
  </div>
`;

export default {
  props: ['id', 'label', 'param', 'options'],
  template,
  methods: {
    onChange: function(e) {
      const input = e.target;
      this.$emit('change', this.param, input.value);
    }
  }
};
