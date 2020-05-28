<template>
  <div class='profile'>
    <div class='card' v-bind:style='{backgroundImage: `url(${currentPhoto})`}'>
      <div class='photo-count-container'>
        <button
          v-for='(photo, index) in allPhotos'
          v-bind:key='index'
          v-bind:selected='index === currentPhotoIndex'
          v-on:click='goToImage(index)'
        ></button>
      </div>
      <div class='photo-buttons'>
        <div class='image-left' v-on:click='previousImage'>👈</div>
        <div class='image-right' v-on:click='nextImage'>👉</div>
      </div>
      <div class='card__body'>
        <div class='card__header'> <!-- contains name, age, distance -->
          <div class='name_and_age'>
            <div class='name'>{{recommendation.user.name}}</div>
            &nbsp;
            <div class='age'>{{age}}</div>
          </div>
          <div class='distance-container'>
            <span class='distance-icon'>📍</span>
            <span class='distance'>{{distance}}</span>
          </div>
        </div>
        <div class='card__content' v-if='recommendation.user.bio'>
          <details>
            <div class='bio' v-html='recommendation.user.bio' v-bind:open='showBio'></div>
          </details>
        </div>
      </div>
    </div>
    <div class='actions'>
      <div class='dislike action' v-on:click='swipe'>🙅‍♂️</div>
      <div class='superlike action' v-on:click='swipe'>😍</div>
      <div class='like action' v-on:click='swipe'>👍</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SwipeCard',
  props: {
    recommendation: Object,
  },
  created() {
    document.addEventListener('keydown', this.onKeyDown);
  },
  watch: {
    recommendation(newVal, prevVal) {
      /* eslint no-underscore-dangle: ['error', { 'allow': ['_id'] }] */
      if (prevVal?.user?._id !== newVal.user._id) {
        this.goToImage(0);
        this.preloadNextImage();
      }
    },
  },
  data: () => ({
    currentPhotoIndex: 0,
    showBio: false,
  }),
  computed: {
    profilePhotos() {
      return this.recommendation.user.photos.map((photo) => photo.url);
    },
    instagramPhotos() {
      let instagramPhotos = [];
      if ('instagram' in this.recommendation && this.recommendation.instagram.media_count > 0) {
        instagramPhotos = this.recommendation.instagram.photos.map((photo) => photo.image);
      }
      return instagramPhotos;
    },
    allPhotos() {
      return this.profilePhotos.concat(...this.instagramPhotos);
    },
    currentPhoto() {
      return this.allPhotos[this.currentPhotoIndex];
    },
    age() {
      const currentYear = (new Date()).getFullYear();
      const birthYear = parseInt(this.recommendation.user.birth_date.substr(0, 4), 10);
      return currentYear - birthYear;
    },
    distance() {
      const ONE_MILE_IN_KM = 1.60934;
      const distance = Math.round(ONE_MILE_IN_KM * this.recommendation.distance_mi);
      return `${distance} km away`;
    },
  },
  methods: {
    onKeyDown(event) {
      let doNothing = true;
      switch (event.key) {
        case 'Down': // IE/Edge specific value
        case 'ArrowDown':
        case 'Up': // IE/Edge specific value
        case 'ArrowUp':
          this.showBio = !this.showBio;
          break;
        case 'Left': // IE/Edge specific value
        case 'ArrowLeft':
          this.$emit('swipe', 'dislike');
          break;
        case 'Right': // IE/Edge specific value
        case 'ArrowRight':
          this.$emit('swipe', 'like');
          break;
        case 'Enter':
          this.$emit('swipe', 'superlike');
          break;
        case '(Space character)': // IE/Edge specific value
        case ' ':
          this.nextImage();
          break;
        case '1':
          this.goToImage(0);
          break;
        default:
          doNothing = false;
      }
      if (doNothing) {
        event.preventDefault();
      }
    },
    goToImage(index) {
      const photoCount = this.allPhotos.length;
      this.currentPhotoIndex = ((index % photoCount) + photoCount) % photoCount;
    },
    nextImage() {
      this.goToImage(this.currentPhotoIndex + 1);
      this.preloadNextImage();
    },
    previousImage() {
      this.goToImage(this.currentPhotoIndex - 1);
    },
    preloadNextImage() {
      const img = document.createElement('img');
      const photoCount = this.allPhotos.length;
      img.src = this.allPhotos[(this.currentPhotoIndex + 1) % photoCount];
    },
    swipe(event) {
      const [swipeDirection] = [...event.target.classList].filter((c) => c !== 'action');
      this.$emit('swipe', swipeDirection);
    },
  },
};
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang='scss'>
.profile{
  height: calc(100vh - 5rem);
  margin: auto 1rem;
  display: flex;
  flex-flow: column nowrap;
  max-width: 75vw;
  .card{
    /* max-width: 25vw; */
    margin: 1rem auto;
    border-radius: 0.5rem;
    box-shadow: 0 2px 10px 0 rgba(84,84,84,0.77);
    /* min-height: 75vh; */
    background-position: center;
    background-size: 100%;
    background-repeat: no-repeat;
    display: flex;
    flex: 1;
    flex-flow: column nowrap;
    background-color: var(--background-color-tinder);
    width: calc(75vw * 0.55);
    max-width: 75vw;
    .photo-count-container{
      display: flex;
      flex-flow: row wrap;
      padding: 0.5rem;
      & > button{
        flex: 1;
        opacity: 0.5;
        background-color: white;
        border-style: none;
        border: 0 !important;
        height: 0.2rem;
        border-radius: 1rem;
        margin: 0.1rem;
        cursor: pointer;
        &[selected]{
          opacity: 1;
        }
      }
    }
    .photo-buttons {
      visibility: hidden;
      flex: 1;
      .image-left, .image-right{
        display: inline-flex;
        flex: 1;
        user-select: none;
        align-items: center;
        margin: 1rem;
      }
      .image-right{
        justify-content: flex-end;
      }
    }
    .card__body{
      background-image: linear-gradient(to bottom, rgba(0,0,0,0), rgba(0,0,0,0.3));
    }
    .card__header{
      color: var(--text-color-flipped);
      display: flex;
      flex-flow: column;
      padding: 1rem;
      .name_and_age{
        margin-bottom: 0.5rem;
        font-size: 1.05rem;
        .name, .age{
          display: inline-block;
        }
        .name{
          font-size: 1.3rem;
          font-weight: bold;
        }
      }
      .distance-icon::after{
        margin-right: 0.3rem;
      }
      .distance{
        font-weight: lighter;
      }
    }
    .card__content{
      color: var(--text-color-flipped);
      padding: 1rem;
      .bio{
        padding: 1rem;
        white-space: pre-wrap;
      }
    }
  }
  .actions{
    display: flex;
    justify-content: center;
    flex-flow: row wrap;
    > div {
      cursor: pointer;
      font-size: 2rem;
      padding: 1rem;
      background-color: var(--background-color-content);
      border-radius: 50%;
      width: 2.5rem;
      text-align: center;
      margin: 0 1rem;
      height: 2.5rem;
      transition-timing-function: ease;
      transition-duration: .25s;
      user-select: none;
      box-shadow: 0 2px 6px 0 rgba(112,125,134,0.14);
      &:hover{
        transform: scale(1.1);
      }
      :active{
        transform: scale(1.1);
      }
    }
  }
}
.card:hover .photo-buttons{
  display: flex;
  visibility: visible!important;
  cursor: pointer;
  align-items: stretch;
}
</style>
