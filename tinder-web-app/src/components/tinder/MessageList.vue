<template>
  <Loading v-if="showMessages"></Loading>
  <div v-else class='message-list'>
    <NotMessagedMatchList></NotMessagedMatchList>
    <MatchMessage
      v-for='match in matches'
      v-bind:key='match.id'
      v-bind:match='match'
    ></MatchMessage>
  </div>
</template>

<script>
import Loading from '@/components/Loading.vue';
import MatchMessage from '@/components/tinder/MatchMessage.vue';
import NotMessagedMatchList from '@/components/tinder/NotMessagedMatchList.vue';

export default {
  name: 'MessageList',
  components: {
    Loading,
    MatchMessage,
    NotMessagedMatchList,
  },
  props: {
    loading: Object,
    messages: Array,
  },
  computed: {
    showMessages() {
      return this.loading.messages || !Object.keys(this.messages || {}).length;
    },
  },
};
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>

</style>
