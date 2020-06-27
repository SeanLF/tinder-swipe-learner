<template>
  <DefaultLayout>
    <div class="hero">
      <h1>Welcome</h1>
    </div>
    <div class="start-swiping">
      <h2>Start Swiping</h2>
    </div>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from '@/components/DefaultLayout.vue';

export default {
  name: 'Home',
  components: {
    DefaultLayout,
  },
};
</script>

<style lang="scss" scoped>
  .hero{
    text-align: center;
    font-size: 3rem;
  }
</style>
