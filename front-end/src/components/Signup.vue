<template>
  <v-layout column style="margin: 20px;">
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Register</h3>
    </v-flex>
    <v-flex xs12 sm6 offset-sm3 mt-3>
      <form>
        <v-layout column>
          <v-flex>
            <v-text-field
              name="username"
              v-model="auth.username"
              label="Username"
              id="username"
              type="username"
              required></v-text-field>
          </v-flex>
          <v-flex>
            <v-text-field
              name="email"
              label="Email"
              id="email"
              type="email"
              :rules="[rules.email]"
              v-model="auth.email"
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
          <v-flex>
            <v-text-field
              name="confirmPassword"
              label="Confirm Password"
              id="confirmPassword"
              type="password"
              v-model="auth.confirmPassword"
              ></v-text-field>
          </v-flex>
          <v-flex>
            <v-radio-group v-model="breeze_card" :mandatory="false">
                <v-radio label="Get a new Breeze Card" value="new_bc"></v-radio>
                <v-radio label="Use my Existing Breeze Card" value="old_bc"></v-radio>
              </v-radio-group>
          </v-flex>
          <v-flex v-if ="breeze_card == 'old_bc'">
            <v-text-field
              name="breezecardid"
              label="Breeze Card ID"
              id="breezecardid"
              type="breezecardid"
              :rules="[rules.breezecard]"
              v-model="auth.breezeID"
              counter=16
              required>
            </v-text-field>
          </v-flex>
          <v-flex style = "padding-bottom: 30px;" class="text-xs-center" mt-5>
            <v-btn primary flat type="submit" v-on:click.prevent="signup">Sign Up</v-btn>
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
      breeze_card : null,
      auth: {"username": '', "email": '', "password": '', "confirmPassword": '', "breezeID": ''},
      response: {},
      rules: {
        required: (value) => !!value || 'Required.',
        email: (value) => {
          const pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Invalid e-mail.'
        },
        breezecard: (value) => {
          const pattern = /\d{16}/g
          return pattern.test(value) || 'Invalid breezecard.'
        },
        notempty: (value) => {
          /^$|\s+/
          const pattern = /^$|\s+/
          return pattern.test(value) || 'Cannot be empty.'
        }
      }
    }
  },
  methods: {
    signup: function() {
      var url = "http://54.173.144.94:5000/register_passenger"

      if (this.breeze_card == 'new_bc') {
        this.auth.breezeID = "NEW_CARD"
      }

      if (this.rules.email(this.auth.email) == 'Invalid e-mail.') {
        alert('Bad Email!')
        return
      } else if (this.auth.username == ''){
        alert('Bad Username!')
        return
      } else if (this.auth.password == '' || this.auth.password.length < 8){
        alert('Bad Password!')
        return
      } else if (this.auth.password != this.auth.confirmPassword){
        alert('Password and Confirm Password are not the same.')
        return
      } else if (this.auth.breezeID != "NEW_CARD" && this.rules.breezecard(this.auth.breezeID) == 'Invalid breezecard.') {
        alert('Bad BreezeID.')
        return
      }

      const vm = this;
      axios.post(url, this.auth)
        .then((response) => {
          if (response.data.code == 200) {
            router.push('/welcomeuser')
            vm.response = response
          } else if (response.data.code == 50) {
            // I made up this code, it's just saying that it's already taken.
            alert('This username has been taken!')
          } else if (response.data.code == 51) {
            alert('This email has been taken!')
          }
        })
        .catch(error => {
          alert('Hmmm something went wrong with our servers!! Sorry!')
      });
    }
  }
}
</script>