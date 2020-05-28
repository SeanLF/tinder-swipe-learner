<template>
  <div class='tinder-app'>
    <TinderSidebar
      v-bind:loading="loading"
      v-bind:profile="profile"
      v-bind:matches="matches"
      v-bind:messages="messages"
    ></TinderSidebar>
    <main>
      <Swiping
        v-bind:loading="loading.recommendations"
        v-bind:recommendation="currentRecommendation"
        v-on:swipe="swipe"
      ></Swiping>
    </main>
    <footer>
      <div class="keyboard-shortcuts">
        <div class="nope">⬅️ Nope</div>
        <div class="super-like">⏎ Super Like</div>
        <div class="like">➡️ Like</div>
        <div class="open-profile">⬆️ Open Profile</div>
        <div class="close-profile">⬇️ Close Profile</div>
        <div class="next-photo">▭ Next photo</div>
        <div class="next-photo">1️⃣ 1st photo</div>
      </div>
    </footer>
  </div>
</template>

<script>
import TinderSidebar from '@/components/tinder/TinderSidebar.vue';
import Swiping from '@/components/tinder/Swiping.vue';

export default {
  name: 'TinderApp',
  components: {
    TinderSidebar,
    Swiping,
  },
  data: () => ({
    apiHostUrl: 'http://localhost:5000',
    apiToken: null,
    loading: {
      recommendations: false,
      matches: false,
      messages: false,
      profile: false,
    },
    error: {
      recommendations: null,
      matches: null,
      messages: null,
      profile: false,
    },
    profile: JSON.parse(localStorage.getItem('profile')),
    recommendations: JSON.parse(localStorage.getItem('recommendations')),
    matches: JSON.parse(localStorage.getItem('matches')),
    messages: JSON.parse(localStorage.getItem('messages')),
  }),
  created() {
    this.apiToken = JSON.parse(localStorage.getItem('apiToken'));
    if (this.apiToken === null) {
      this.$router.push('/login/sms');
    } else {
      this.fetchData();
    }
  },
  watch: {
    $route: 'fetchData',
    recommendations() {
      if (this.recommendations.length < 2) {
        this.fetchRecommendations();
      }
    },
  },
  computed: {
    currentRecommendation() {
      return this.recommendations !== null && this.loading.recommendations === false
        ? this.recommendations[0] : {};
    },
  },
  methods: {
    fetchData() {
      this.loading = {
        recommendations: false,
        matches: false,
        messages: false,
        profile: false,
      };
      this.error = {
        recommendations: null,
        matches: null,
        messages: null,
        profile: false,
      };
      this.fetchProfile();
      if (this.recommendations === null || this.recommendations?.length < 2) {
        this.fetchRecommendations();
      }
      this.fetchMatches();
      this.fetchMessages();
    },
    fetchProfile() {
      fetch(`${this.apiHostUrl}/tinder/profile`, {
        method: 'GET',
        headers: {
          'X-Auth-Token': this.apiToken,
          'content-type': 'application/json',
        },
      }).then((resp) => resp.json())
        .then(this.setProfile);
    },
    setProfile(data) {
      this.profile = data;
      this.loading.profile = false;
    },
    fetchRecommendations() {
      fetch(`${this.apiHostUrl}/tinder/recommendations`, {
        method: 'GET',
        headers: {
          'X-Auth-Token': this.apiToken,
          'content-type': 'application/json',
        },
      }).then((resp) => resp.json())
        .then(this.setRecommendations);
    },
    setRecommendations(data) {
      const recommendations = this.recommendations || [];
      this.recommendations = recommendations.concat(...(data));
      this.loading.recommendations = false;
    },
    fetchMatches(limit = 10) {
      fetch(`${this.apiHostUrl}/tinder/matches`, {
        method: 'GET',
        headers: {
          'X-Auth-Token': this.apiToken,
          'content-type': 'application/json',
        },
        data: JSON.stringify({ limit, pageToken: this.pageToken }),
      }).then((resp) => resp.json())
        .then(this.setMatches);
    },
    setMatches(data) {
      const matches = this.matches || [];
      const [dataMatches, pageToken] = data;
      this.matches = matches.concat(...(dataMatches));
      this.pageToken = pageToken;
      this.loading.matches = false;
    },
    fetchMessages() {
      this.messages = [];
      this.loading.messages = false;
    },
    swipe(swipeDirection) {
      fetch(`${this.apiHostUrl}/tinder/swipe`, {
        method: 'POST',
        headers: {
          'X-Auth-Token': this.apiToken,
          'content-type': 'application/json',
        },
        body: JSON.stringify({
          /* eslint no-underscore-dangle: ["error", { "allow": ["_id"] }] */
          id: this.currentRecommendation.user._id,
          action: swipeDirection,
        }),
      }).then((resp) => resp.json())
        .then((data) => {
          if (data.data?.match) {
            alert('You have a new match');
          }
        });
      this.recommendations.shift();
    },
  },
};
</script>

<style lang='scss' scoped>
.tinder-app{
  display: grid;
  grid-template-areas:
    'sidebar main'
    'sidebar footer';
  height: 100vh;
}
.tinder-sidebar{
  grid-area: sidebar;
}
main{
  grid-area: main;
  display: flex;
  width: 100vw;
  max-width: calc(75vw - 1px);
  border-left: 1px solid var(--border-color);
  flex-grow: 1;
  flex-flow: column nowrap;
  overflow-y: scroll;
}
footer{
  grid-area: footer;
}
.keyboard-shortcuts {
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
  align-items: center;
  margin: 1rem;
  & > div {
    margin-right: 1rem;
    color: var(--text-color-light);
    user-select: none;
  }
}
</style>
