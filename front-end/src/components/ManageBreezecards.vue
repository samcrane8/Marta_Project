<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Manage Breezecards</h3>
    </v-flex>
    <v-card style="margin:20px;" flat>
      <v-card-title style="margin-left:20%;margin-right:20%;">
        <v-text-field
          append-icon="search"
          label="Search"
          single-line
          hide-details
          v-model="search"
        ></v-text-field>
      </v-card-title>
      <v-data-table
          v-bind:headers="headers"
          v-bind:items="items"
          v-bind:search="search"
          item-key="card_id"
          class="elevation-1"
        >
        <template slot="items" slot-scope="props">
		  <tr @click="props.expanded = !props.expanded; expand_card(props.item);">
            <td>{{ props.item.card_id }}</td>
            <td class="text-xs-center">${{ props.item.value }}</td>
          </tr>
        </template>
        <template slot="pageText" slot-scope="{ pageStart, pageStop }">
          From {{ pageStart }} to {{ pageStop }}
        </template>
        <template slot="expand" slot-scope="props">
	      <v-card>
	      	<v-card-title>
	          <h3 class="headline mb-0">Manage Card: {{props.item.card_id}}</h3>
	        </v-card-title>
	        <v-card-text>
		          <v-layout row>
	              <v-subheader>Add Value</v-subheader>
	              <v-text-field
	                label="Amount"
	                v-model = "card_update.value"
	                prefix="$"
	              ></v-text-field>
		          </v-layout>
		        </v-card-text>
		        <v-card-actions>
				  <v-flex>
				     <v-btn flat color="blue" @click="props.expanded = false; update_card(props.item)">UPDATE</v-btn>
			   	  </v-flex>
			  </v-card-actions>
	      </v-card>
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
  data () {
    return {
      max25chars: (v) => v.length <= 25 || 'Input too long!',
      tmp: '',
      search: '',
      pagination: {},
      headers: [
        { text: 'Card ID', value: 'card_id', align: 'left'},
        { text: 'Value', value: 'value', align: 'center'}
      ],
      items: [],
      card_update: {
      	card_id: '',
      	value: 0,
      	owner: ''
      }
    }
  },
  methods: {
  	refresh_breezecards() {
    	//now this is going to be run when they mount.
	    var url = "http://54.173.144.94:5000/get_breezecards"
	    axios.get(url)
	        .then((response) => {
	          this.items = response.data
	        })
	        .catch(error => {
	          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
	    });
    },
    update_card(item) {
    	//now this is going to be run when they mount.
	    var url = "http://54.173.144.94:5000/update_card"
    	alert(JSON.stringify(this.card_update))
    	this.card_update.owner = item.owner
    	this.card_update.card_id = item.card_id
	    axios.post(url, this.card_update)
	        .then((response) => {
	          this.refresh_breezecards()
	          this.card_update.value = 0
	        })
	        .catch(error => {
	          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
	    });
    }
  },
  beforeMount() {
  	this.refresh_breezecards()
  }
}
</script>