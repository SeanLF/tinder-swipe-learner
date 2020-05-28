<template>
  <aside class='tinder-sidebar'>
    <nav class='nav'>
      <div class='brandbar'>
        <div class='my-profile'>
          <img v-bind:src='profileImage' alt='My Profile' height='' width=''>
          <span class='my-profile__header'>My Profile</span>
        </div>
      </div>
      <div class='aside-navbar'>
        <div class='matches-nav-link'
          v-on:click='matchList'
          v-bind:aria-selected='matchesSelected'
        >
          <span class='title'>Matches</span>
          <div class='count-bubble' v-if='hasMatches'>
            <span class='count'>{{matchesCount}}</span>
          </div>
        </div>
        <div class='messages-nav-link'
          v-on:click='messageList'
          v-bind:aria-selected='!matchesSelected'
        >
          <span class='title'>Messages</span>
          <div class='count-bubble' v-if='hasMessages'>
            <span class='count'>{{messages.length}}</span>
          </div>
        </div>
      </div>
    </nav>
    <div class='aside-content'>
        <component
          v-bind:is='currentNavComponent'
          v-bind='currentProperties'
          v-bind:loading='loading'
        ></component>
    </div>
  </aside>
</template>

<script>
import MatchList from '@/components/tinder/MatchList.vue';
import MessageList from '@/components/tinder/MessageList.vue';

export default {
  name: 'TinderSidebar',
  components: {
    MatchList,
    MessageList,
  },
  data: () => ({
    currentNavComponent: MatchList,
  }),
  props: {
    loading: Object,
    profile: Object,
    matches: Array,
    messages: Array,
  },
  computed: {
    profileImage() {
      return this.loading.profile || !this.profile ? '' : this.profile.photos[0].processedFiles[3].url;
    },
    hasMatches() {
      return !this.loading.matches && this.matches && this.matches.length > 0;
    },
    matchesCount() {
      let matchesCount = this.matches.length;
      if (matchesCount >= 99) {
        matchesCount += '+';
      }
      return matchesCount;
    },
    matchesSelected() {
      return this.currentNavComponent === MatchList;
    },
    hasMessages() {
      return !this.loading.messages && this.messages.length > 0;
    },
    currentProperties() {
      return this.currentNavComponent === MatchList
        ? { matches: this.matches } : { messages: this.messages };
    },
  },
  methods: {
    matchList() {
      this.currentNavComponent = MatchList;
    },
    messageList() {
      this.currentNavComponent = MessageList;
    },
  },
};
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>
.tinder-sidebar{
  width: 25vw;
  min-width: 19rem;
  display: flex;
  flex-flow: column;
  max-height: 100vh;
  background-color: var(--background-color-content);
  & > .nav{
    display: fixed;
    user-select: none;
    & > .brandbar{
      background-image: var(--background-image-tinder);
      color: var(--text-color-flipped);
      padding: 1.2rem 1.4rem;
      font-size: 1.4rem;
      box-shadow: 0 1px 8px 0 rgba(0,17,25,.27);
      & > .my-profile{
        display: flex;
        align-items: center;
        & > img {
          border-radius: 50%;
          height: 2rem;
          width: 2rem;
          border: 2px solid white;
          margin-right: 1rem;
          box-shadow: 0 1px 5px 0 hsla(0,0%,42.7%,.56);
          & .my-profile__header{
            font-weight: lighter;
          }
        }
      }
    }
    & > .aside-navbar{
      display: flex;
      flex-flow: row wrap;
      justify-content: space-evenly;
      padding: 1rem 0;
      box-shadow: 0 1px 8px 0 rgba(0,17,25,.27);
      & > .matches-nav-link, & > .messages-nav-link{
        display: flex;
        align-items: center;
        cursor: pointer;
        padding-bottom: 0.2rem;
        border-bottom: 0.2rem transparent;
        &[aria-selected=true]{
          border-bottom: 0.2rem solid var(--background-color-tinder);
        }
        & > .title{
          font-weight: bold;
        }
        & > .count-bubble{
          display: inline-block;
          border-radius: 5rem;
          margin-left: 0.2rem;
          height: 1.2rem;
          width: 1.2rem;
          background-color: var(--background-color-tinder);
          text-align: center;
          color: var(--text-color-flipped);
          & > .count {
          font-size: 0.8rem;
          }
        }
      }
    }
  }
  & > .aside-content{
    display: flex;
    flex-flow: row wrap;
    justify-content: space-evenly;
    overflow-y: scroll;
    padding-top: 0.5rem;
  }
}
</style>
