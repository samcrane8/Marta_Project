<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Trip History</h3>
    </v-flex>
    <v-card style="margin: 20px; padding: 5px;">
      <v-card-title>
        <h5 class="text-xs-left">Trip History</h5>
      </v-card-title>
      <v-layout row wrap>
        <v-flex xs11 sm5>
          <v-menu
            lazy
            :close-on-content-click="false"
            v-model="start_picker.menu"
            transition="scale-transition"
            offset-y
            full-width
            :nudge-right="40"
            max-width="290px"
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              label="Start Date"
              :close-on-click = "false"
              v-model="start_picker.date"
              prepend-icon="event"
              readonly
            ></v-text-field>
            <v-date-picker v-model="start_picker.date" no-title scrollable actions>
            </v-date-picker>
          </v-menu>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs11 sm5>
          <v-menu
            lazy
            :close-on-content-click="false"
            v-model="end_picker.menu"
            transition="scale-transition"
            offset-y
            full-width
            :nudge-right="40"
            max-width="290px"
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              label="End Date"
              v-model="end_picker.date"
              prepend-icon="event"
              readonly
            ></v-text-field>
            <v-date-picker v-model="end_picker.date" no-title scrollable autosave>
            </v-date-picker>
          </v-menu>
        </v-flex>
      <v-card-actions class="text-xs-left">
        <v-flex>
            <v-btn primary flat type="submit" v-on:click="trip_history()">REFRESH</v-btn>
          </v-flex>
      </v-card-actions>
    </v-layout>
    <v-data-table
          :headers="headers"
            :search="search"
          :items="items"
          item-key="station_name"
          hide-actions
          class="elevation-1"
        >
        <template slot="items" slot-scope="props">
          <tr @click="props.expanded = !props.expanded">
            <td>{{ props.item.time }}</td>
            <td class="text-xs-center">{{ props.item.source }}</td>
            <td class="text-xs-center">{{ props.item.destination }}</td>
            <td class="text-xs-center">{{ props.item.fare_paid }}</td>
            <td class="text-xs-center">${{ props.item.card_id }}</td>
        </tr>
        </template>
      </v-data-table>
    </v-card>
  </v-layout>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from '@/router'
 
Vue.use(VueAxios, axios)

export default {
  props: ['user'],
  data () {
      return {
        search: '',
        headers: [
          {text: 'Time', value: 'time', align: 'left'},
          { text: 'Source', value: 'source', align: 'center'},
          { text: 'Destination', value: 'destination', align: 'center'},
          { text: 'Fare Paid', value: 'fare_paid', align: 'center'},
          { text: 'Card #', value: 'card_id', align: 'center'}
        ],
        trips: [],
        start_picker: {
          date: '2017-10-1',
          menu: false
        },
        end_picker: {
          date: '2017-12-25',
          menu: false 
        }
      }
  },
  methods: {
      trip_history() {
        //now this is going to be run when they mount.
        var url = "http://54.173.144.94:5000/trip_history"
        if (this.user == null) {
          this.$emit('logout')
          this.$emit('goHome')
        }
        var body = {
          "username": this.user.auth.username,
          "start_time": this.start_picker.date,
          "end_time": this.end_picker.date
        }

        axios.post(url, body)
            .then((response) => {
              this.trips = response.data
            })
            .catch(error => {
              alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
          });
      },
      refresh_breezecards() {
        //now this is going to be run when they mount.
        var url = "http://54.173.144.94:5000/get_user_breezecards"
        if (this.user == null) {
          this.$emit('logout')
          this.$emit('goHome')
        }
          var body = {
             "owner":this.user.auth.username
          }
        axios.post(url, body)
            .then((response) => {
              this.breezecards = response.data
            })
            .catch(error => {
              alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
        });
      }
  },
    beforeMount(){
      this.refresh_breezecards()
      this.trip_history()
    }
}
</script>