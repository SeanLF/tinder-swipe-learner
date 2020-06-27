<template>
  <div class="DefaultLayout">
    <Header></Header>
    <main class="main">
      <slot/>
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';

export default {
  name: '',
  components: {
    Header,
    Footer,
  },
};

</script>
