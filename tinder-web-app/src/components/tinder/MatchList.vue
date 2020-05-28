<template>
  <Loading v-if="showMatches"></Loading>
  <div class='match-list' v-else>
    <MatchCard
      v-for='match in matches'
      v-bind:key='match.id'
      v-bind:match='match'
    ></MatchCard>
  </div>
</template>

<script>
import Loading from '@/components/Loading.vue';
import MatchCard from '@/components/tinder/MatchCard.vue';

export default {
  name: 'MatchList',
  props: {
    loading: Object,
    matches: Array,
  },
  computed: {
    showMatches() {
      return this.loading.matches || !Object.keys(this.matches || {}).length;
    },
    matchCount() {
      let matchCount = this.matches.length;
      if (matchCount === 99) matchCount += '+';
      return matchCount;
    },
    hasMatches() {
      return this.matches.length > 0;
    },
  },
  components: {
    Loading,
    MatchCard,
  },
};
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>
.match-list{
  display: flex;
  flex-flow: row wrap;
  justify-content: space-evenly;
  overflow-y: scroll;
  padding-top: 0.5rem;
  &::after{
    content: '';
    display: block;
    height: 1rem;
    width: 100%;
  }
}
</style>
