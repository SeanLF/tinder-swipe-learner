<template>
  <header class="header">
    <nav class="nav">
      <div class="brand-bar">
        <h1>Tinder #machine-learning</h1>
      </div>
      <div class="navigation-bar">
        <a href="https://tinder.com">Official Tinder</a>
        <router-link to="/">Home</router-link>
        <router-link to="/about">About</router-link>
        <router-link to="/login/sms">Login via SMS</router-link>
        <router-link to="/Tinder">Tinder</router-link>
      </div>
    </nav>
  </header>
</template>
<script>
export default {
  name: 'Header',
  props: {
  },
};
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.header{
  display: flex;
  border-bottom: 1px solid var(--border-color);
}
.nav{
  display: flex;
  flex: 1;
  flex-flow: column nowrap;
  align-items: stretch;
}
.brand-bar{
  text-align: center;
  background: var(--background-image-tinder);
  color: var(--text-color-flipped);;
  & > h1{
    font-size: 1.5rem;
    margin: 1rem auto;
  }
}
.navigation-bar{
  display: flex;
  flex-flow: row nowrap;
  overflow-x: scroll;
  background-color: var(--background-color-content);

  & > a{
    padding: 1rem;
    flex-shrink: 0;
    text-decoration: none;
    color: var(--text-color);
    &:hover{
      background-color: var(--background-color);
    }
    &.router-link-exact-active{
      background-color: var(--background-color-selected);
    }
  }
}
</style>
