<template>
  <div class='match-message-item'>
    <div class='photo'>{{photo}}</div>
    <div class='content'>
      <div class='name-container'>
        <span class='unseen' v-if='unseen'></span>
        <span class='name'>{{name}}</span>
      </div>
      <div class='message'>{{message}}</div>
    </div>
    <div class='unseen' v-if='match.match_seen'></div>
    <div class='match-card__content'>
      <span class='match-name'>{{match.person.name}}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MatchCard',
  props: {
    match: Object,
    message: String,
  },
  computed: {
    photo: () => (this.match.person.photos[0].processedFiles[2]),
    photoInlineStyles: () => ({
      'background-image': `url(${this.photo.url})`,
      height: this.photo.height,
      width: this.photo.width,
    }),
  },
};
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>
.match-card {
  color: var(--text-color-flipped);
  margin-bottom: 0.5rem;
  border-radius: 3px;
  cursor: pointer;
  display: flex;
  align-items: flex-end;
  min-width: 30%;
  max-width: 50%;
  height: 130px;
  overflow: hidden;
  box-shadow: 3px 3px 3px 0 rgba(84, 84, 84, 0.77);

  & > .match-card__content {
    background-repeat: no-repeat;
    transition-duration: 0.25s;
    background-size: 110%;
    background-position: center;
    height: 100%;
    width: 100%;
    display: flex;
    align-items: end;

    &:first-child:hover {
      transform: scale(1.1);
    }
  }
  > span {
    padding: 5px;
    user-select: none;
  }
}
.unseen {
  background-color: var(--background-color-tinder);
  width: 0.5rem;
  height: 0.5rem;
  &::after {
    content: ' ';
  }
}
</style>
