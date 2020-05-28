<template>
  <form
    v-on:submit="submit"
  >
    <div class='single-input-form'>
      <label v-bind:for='form.fieldClass'>{{form.fieldLabel}}</label>
      <input
        class="input"
        v-bind:type='form.inputType'
        v-bind:name='form.fieldClass'
        v-bind:id='form.fieldClass'
        required
        v-bind:value="form.value"
      />
      <div class='submit_wrapper'>
        <input type='submit' value='↑' class='submit' />
      </div>
    </div>
  </form>
</template>
<script>
export default {
  name: 'SingleInputForm',
  props: {
    form: Object,
  },
  methods: {
    submit(event) {
      this.$emit('submit', event);
    },
  },
};
</script>
<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>
.single-input-form {
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  margin: 1rem auto;
  font-size: 1.1rem;
  & .input {
    flex: 1;
    border: 2px solid var(--border-color);
    border-radius: 2rem;
    margin: auto -2rem auto 1rem;
    padding: 0.5rem 1rem;
    font-size: 1.15rem;
    &:focus {
      outline: none;
      border: 2px solid var(--background-color-tinder);
    }
  }
  .submit_wrapper {
    z-index: 2;
    position: relative;
    right: 0.4rem;
    height: 2rem;
    width: 2rem;
    border-radius: 2rem;
    background: var(--background-image-tinder);
    .submit {
      position: relative;
      display: flex;
      justify-content: center;
      height: 3rem;
      width: 3rem;
      bottom: 0.5rem;
      right: 0.5rem;
      cursor: pointer;
      border: none;
      color: var(--text-color-flipped);
      font-size: 1.1rem;
      background: transparent;
      transition-timing-function: ease;
      transition-duration: 0.25s;
      &:active {
        transform: translateY(-1rem);
        opacity: 0;
      }
    }
  }
}
</style>
