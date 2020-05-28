<template>
  <div class='swiping'>
    <Loading v-if="showLoading">
      Loading...
    </Loading>
    <SwipeCard v-bind:recommendation="recommendation" v-on:swipe="swipe" v-else/>
  </div>
</template>

<script>
import Loading from '@/components/Loading.vue';
import SwipeCard from '@/components/tinder/SwipeCard.vue';

export default {
  name: 'Swiping',
  components: {
    Loading,
    SwipeCard,
  },
  props: {
    loading: Boolean,
    recommendation: Object,
  },
  computed: {
    showLoading() {
      return this.loading || !Object.keys(this.recommendation).length;
    },
  },
  methods: {
    swipe(swipeDirection) {
      this.$emit('swipe', swipeDirection);
    },
  },
};
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>
.swiping{
  display: flex;
  flex-flow: column nowrap;
  background-color: var(--background-color);
  .loading{
    height: calc(100vh - 5rem);
    display: flex;
    max-width: 75vw;
    justify-content: center;
  }
}
</style>
