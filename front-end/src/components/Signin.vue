<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Login</h3>
    </v-flex>
    <v-flex xs12 sm6 offset-sm3 mt-3>
      <form style="margin: 20px">
        <v-layout column>
          <v-flex>
            <v-text-field
              name="username"
              label="Username"
              id="username"
              type="username"
              v-model="auth.username"
              required></v-text-field>
          </v-flex>
          <v-flex>
            <v-text-field
              name="password"
              label="Password"
              id="password"
              type="password"
              v-model="auth.password"
              required></v-text-field>
          </v-flex>
          <v-flex class="text-xs-center" mt-5>
            <v-btn primary flat type="submit" @click.prevent = "login">Sign In</v-btn>
          </v-flex>
        </v-layout>
      </form>
    </v-flex>
  </v-layout>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from '@/router'
 
Vue.use(VueAxios, axios)

export default {
  data() {
    return {
      auth: {"username": '', "password": ''},
      response: {},
    }
  },
  methods: {
    login: function() {

      var url = "http://54.173.144.94:5000/login"
      const vm = this;

      var credentials = btoa(this.auth.username + ':' + this.auth.password);
      var BasicAuth = 'Basic ' + credentials;
      axios.get(url, {
        headers: {'Authorization': BasicAuth}
      })
        .then((response) => {
          if (response.data.code == 200) {
            var userinfo = {
              auth: vm.auth,
              isadmin: response.data.isAdmin
            }
            vm.$emit('login',userinfo)
          } else {
            alert('Bad Login!')
          }
        })
        .catch(error => {
          alert('Hmmm something went wrong with our servers!! Sorry!')
      });
    }
  }  
}
</script>