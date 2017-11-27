<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Station Management</h3>
    </v-flex>
    <v-card v-if="!new_station" style="margin: 20px; padding: 5px;" flat>
    	<v-card-title class = "text-xs-center" style="margin-left: 20%;margin-right: 20%;">
	        <v-text-field
	        append-icon="search"
	        label="Search"
	        single-line
	        hide-details
	        v-model="search"
	      ></v-text-field>
	    </v-card-title>
	    <v-data-table
	        :headers="headers"
	        :search="search"
	        :items="items"
      		item-key="station_name"
	        hide-actions
	        class="elevation-1"
	      >
	      <template slot="items" slot-scope="props" flat>
	      	<tr @click="props.expanded = !props.expanded; expand_station(props.item)">
		        <td>{{ props.item.station_name }}</td>
		        <td class="text-xs-center">{{ props.item.stop_id }}</td>
		        <td class="text-xs-center">{{ props.item.fare }}</td>
		        <td class="text-xs-center">{{ props.item.isopen }}</td>
		      </tr>
	      </template>
		    <template slot="expand" slot-scope="props">
		      <v-card>
		      	<v-card-title>
		          <h3 class="headline mb-0">Station Details: {{props.item.station_name}}</h3>
		        </v-card-title>
		        <v-card-text>
		          <v-layout row>
	              <v-subheader>Update Fare</v-subheader>
	              <v-text-field
	                label="Amount"
	                v-model = "station_details.updated_fare"
	                :value = "props.item.station_name"
	                prefix="$"
	              ></v-text-field>
                <v-spacer/>
		          </v-layout>
		        	<v-layout row>
		            <v-subheader v-if ="station_details.isBus">Nearest Intersection: </v-subheader>
		            <v-subheader style="color:grey;">{{props.item.nearest_intersection}} </v-subheader>
		            <v-spacer v-if ="station_details.isBus"/>
		            <v-subheader>Is Open: </v-subheader>
						    <v-checkbox
                  color="green"
                  v-model="station_details.isopen"
                  hide-details></v-checkbox>
		          </v-layout>
		        </v-card-text>
		        <v-card-actions>
						  <v-flex>
							  <v-btn flat color="blue" @click="props.expanded = false; update_station()">UPDATE</v-btn>
					    </v-flex>
					  </v-card-actions>
		      </v-card>
		    </template>
	    </v-data-table>
	    <v-card-actions>
	    	<v-flex>
	          <v-btn flat color="blue" @click.prevent="new_station = true">Create New Station</v-btn>
	      </v-flex>
	    </v-card-actions>
	</v-card>
	<v-card v-if="new_station" style="margin: 20px; padding: 20px;">
		<v-layout column>
		 <h3 class="headline mb-0">Create New Station</h3>
          <v-flex>
            <v-text-field
              name="station_name"
              label="Station Name"
              id="station_name"
              type="username"
              v-model="new_stat_vals.station_name"
              required>
              </v-text-field>
          </v-flex>
          <v-flex>
            <v-text-field
              name="stop_id"
              label="Stop ID"
              id="stop_id"
              type="username"
              v-model="new_stat_vals.stopid"
              required>
              </v-text-field>
          </v-flex>
          <v-flex>
            <v-text-field
              name="fare"
              label="Fare"
              id="fare"
              type="username"
              v-model="new_stat_vals.fare"
              required>
              </v-text-field>
          </v-flex>
          <v-flex>
            <v-radio-group v-model="new_stat_vals.isbus" :mandatory="false">
                <v-radio label="Train Station" :value="false"></v-radio>
                <v-radio label="Bus Station" :value="true"></v-radio>
              </v-radio-group>
          </v-flex>
          <v-flex v-if ="new_stat_vals.isbus">
            <v-text-field
              name="nearest_intersection"
              label="Nearest Intersection"
              id="nearest_intersection"
              type="username"
              v-model="new_stat_vals.nearest_intersection"
              required>
            </v-text-field>
          </v-flex>
        </v-layout>
			<v-card-actions>
	        <v-flex>
	        	<v-btn flat color="green" @click="save_station">Save</v-btn>
	        </v-flex>
	    	<v-flex class="text-xs-right">
	        	<v-btn flat @click.prevent="new_station = false" color="red">Cancel</v-btn>
	        </v-flex>
	    </v-card-actions>
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
	data () {
    return {
    	search: '',
    	new_station: false,
      headers: [
      {text: 'Station Name', value: 'station_name', align: 'left'},
      { text: 'Stop ID', value: 'stop_id', align: 'center'},
      { text: 'Fare', value: 'fare', align: 'center' },
      { text: 'Status', value: 'isopen', align: 'center' }
      ],
      items: [],
      new_stat_vals: {
    	  station_name: '',
    	  stop_id: null,
    	  fare: null,
    	  isbus: false,
    	  isopen: true,
    	  nearest_intersection: ''
      },
      station_details: {
      	stop_id: null,
      	updated_fare: 0,
      	isopen: false,
      	isbus: false
      }
    }
  },
  methods:{
  	save_station() {
  		var url = "http://54.173.144.94:5000/add_station"
    	axios.post(url, this.new_stat_vals)
	        .then((response) => {
	        	this.new_station = false
	        })
	        .catch(error => {
	          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
	      });
  	},
  	refresh_stations() {
  		//now this is going to be run when they mount.
    	var url = "http://54.173.144.94:5000/get_stations"

    	axios.get(url)
	        .then((response) => {
	          var stations = response.data
	          this.items = stations
	        })
	        .catch(error => {
	          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
	      });
  	},
  	update_station() {
  		var url = "http://54.173.144.94:5000/update_station"

    	axios.post(url, this.station_details)
	        .then((response) => {
	    			this.refresh_stations()
	        })
	        .catch(error => {
	          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
	    });
  	},
  	expand_station(item) {
  		this.station_details.stop_id = item.stop_id
  		this.station_details.updated_fare = item.fare
  		if (item.isopen == "OPEN"){
  			this.station_details.isopen = true
  		} else {
  			this.station_details.isopen = false
  		}
  		if (item.nearest_intersection == ''){
  			this.station_details.isBus = false
  		} else {
  			this.station_details.isBus = item.isBus
  		}
  	}
  },
  beforeMount(){
    this.refresh_stations()
  }
}
</script>