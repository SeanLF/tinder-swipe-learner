<template>
  <div class='match-card'>
    <div class='unseen' v-if='!match.seen.match_seen'></div>
    <div class='match-card__content' v-bind:style='photoInlineStyles'>
      <span class='match-name'>{{match.person.name}}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MatchCard',
  props: {
    match: Object,
  },
  computed: {
    photo() {
      return this.match.person.photos[0].processedFiles[2];
    },
    photoInlineStyles() {
      return {
        'background-image': `url(${this.photo.url})`,
        height: this.photo.height,
        width: this.photo.width,
      };
    },
  },
};
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>
.match-card {
  color: var(--text-color-flipped);
  margin-bottom: 0.5rem;
  border-radius: .5rem;
  cursor: pointer;
  display: flex;
  align-items: flex-end;
  min-width: 30%;
  max-width: 50%;
  height: 8.5rem;
  box-shadow: 3px 3px 3px 0 rgba(84, 84, 84, 0.77);
  position: relative;

  & > .match-card__content {
    background-repeat: no-repeat;
    background-size: 110%;
    background-position: center;
    border-radius: 0.5rem;
    height: 100%;
    width: 100%;
    display: flex;
    align-items: flex-end;
    & > span {
      padding: 5px;
      user-select: none;
    }
  }
}
.unseen {
  background-color: var(--background-color-tinder);
  position: absolute;
  top: -0.3em;
  right: -0.3rem;
  border-radius: 1rem;
  height: 0.6rem;
  width: 0.6rem;
  border: 0.2rem solid white;
  &::after {
    content: ' ';
  }
}
</style>
