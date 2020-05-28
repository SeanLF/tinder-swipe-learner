<template>
  <div class='sms'>
    <Header></Header>
    <main class='main'>
      <div class="error" v-if="error !== null">{{error}}</div>
      <SingleInputForm
        v-bind:form=currentView
        v-on:submit="submit"
      ></SingleInputForm>
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import SingleInputForm from '@/components/SingleInputForm.vue';
import Footer from '@/components/Footer.vue';

export default {
  name: 'LoginViaSMS',
  components: {
    Header,
    SingleInputForm,
    Footer,
  },
  data: () => ({
    error: null,
    currentViewKey: 'requestOTP',
    apiHostUrl: 'http://localhost:5000',
    phoneNumber: JSON.parse(localStorage.getItem('phoneNumber')),
    requestOTP: {
      action: 'tinder/login/sms',
      method: 'post',
      fieldLabel: 'Phone Number',
      fieldClass: 'phone-number',
      inputType: 'tel',
      value: null,
    },
    sendOTP: {
      action: 'tinder/login/sms/otp',
      method: 'post',
      fieldLabel: 'OTP Code',
      fieldClass: 'otp-code',
      inputType: 'number',
      value: null,
    },
  }),
  computed: {
    currentView() {
      return this[this.currentViewKey];
    },
  },
  methods: {
    submit(event) {
      event.preventDefault();
      this.error = null;
      let body = {};
      let callback = null;
      if (this.currentViewKey === 'requestOTP') {
        this.phoneNumber = event.target[0].value;
        body = { phone_number: this.phoneNumber };
        callback = this.requestedOTP;
      } else {
        body = { phone_number: this.phoneNumber, otp_code: event.target[0].value };
        callback = this.submittedOTP;
      }
      fetch(`${this.apiHostUrl}/${this.currentView.action}`, {
        method: this.currentView.method,
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body),
      }).then((resp) => resp.json())
        .then(callback);
    },
    requestedOTP(data) {
      if (data.data.sms_sent) {
        this.currentViewKey = 'sendOTP';
      } else {
        this.error = 'An error occured. Please try again.';
      }
    },
    submittedOTP(data) {
      if ('refresh_token' in data) {
        localStorage.setItem('refreshToken', JSON.stringify(data.refresh_token));
        localStorage.setItem('apiToken', JSON.stringify(data.api_token));
        this.$router.push('/Tinder');
      } else {
        this.error = 'An error occured. Please try again.';
      }
    },
  },
};
</script>

<style scoped lang='scss'>
.login-via-sms {
  min-width: 500px;
  width: 50vw;
  margin: 1rem auto;
  min-height: calc(100vh - 12.1rem);
}
</style>
