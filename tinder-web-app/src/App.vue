<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style lang="scss">
html {
  --background-color: #f5f7fa;
  --background-color-selected: #eff1f5;
  --background-color-dark: #363636;
  --background-color-dark-selected: #494949;
  --background-color-dark-lighter: #696969;
  --background-color-content: #ffffff;
  --background-image-tinder: linear-gradient(262deg, #ff7854, #fd267d);
  --background-color-tinder: #fd5068;
  --border-color: #e0e4e9;
  --text-color: #2c2c2c;
  --text-color-light: #545454;
  --text-color-flipped: #ffffff;
  font-family: ProximaNova, sans-serif;
  font-size: 100%;
  text-rendering: optimizeLegibility;
}
body{
  margin: initial;
  background-color: var(--background-color);
  display: flex;
  flex-flow: column nowrap;
  color: var(--text-color);
}
.main{
  min-width: 500px;
  width: 50vw;
  margin: 2rem auto;
  min-height: calc(100vh - 13.8rem);
}
</style>
