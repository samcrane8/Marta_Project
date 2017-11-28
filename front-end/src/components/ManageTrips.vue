<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Manage Trips</h3>
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
	          <v-btn primary flat type="submit" v-on:click="refresh_flow_report()">REFRESH</v-btn>
	        </v-flex>
		  </v-card-actions>
	  </v-layout>
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
	        {text: 'Station Name', value: 'station_name', align: 'left'},
	        { text: 'Passengers In', value: 'pass_in', align: 'center'},
	        { text: 'Passengers Out', value: 'pass_out', align: 'center'},
	        { text: 'Flow', value: 'flow', align: 'center'},
	        { text: 'Revenue', value: 'revenue', align: 'center'}
	      ],
	      items: [],
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
		refresh_flow_report() {
    		//now this is going to be run when they mount.
	    	var url = "http://54.173.144.94:5000/get_flow_report"
	    	var body = {
	    		"start_date": this.start_picker.date,
	    		"end_date": this.end_picker.date
	    	}
	    	axios.post(url, body)
		        .then((response) => {
		          this.items = response.data
		        })
		        .catch(error => {
		          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
		      });
    	}
	},
    beforeMount(){
    	this.refresh_flow_report()
    }
}
</script>