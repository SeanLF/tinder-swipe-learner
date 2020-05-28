<template>
  <footer class="footer">
      <a href="https://seanfloyd.ca">Sean Floyd</a>
    </footer>
</template>

<script>

export default {
  name: 'Footer',
};
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>
.footer{
  display: flex;
  flex-flow: row nowrap;
  overflow-x: scroll;
  border-top: 1px solid var(--border-color);
  background-color: var(--background-color-dark);
  & > a{
    padding: 1rem;
    flex-shrink: 0;
    text-decoration: none;
    color: var(--text-color-flipped);
    &:hover{
      background-color: var(--background-color-dark-lighter);
    }
    &.router-link-exact-active{
      background-color: var(--background-color-dark-selected);
    }
  }
}
</style>
