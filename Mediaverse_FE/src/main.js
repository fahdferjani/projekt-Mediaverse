import './app.css';
import App from './App.svelte';

const app = new App({
  target: document.getElementById('app'),
  //target: document.body,
});

export default app


// main.js
import { sharedValue1, sharedValue2, sharedValue3, sharedValue4, sharedValue5, sharedValue6, sharedValue7, sharedValue8, sharedValue9, sharedValue10 } from './store.js';

// Generiere die Variable in der Hauptdatei
sharedValue1.set('undefined');
sharedValue2.set('undefined');
sharedValue3.set('undefined');
sharedValue4.set('undefined');
sharedValue5.set('undefined');
sharedValue6.set('undefined');
sharedValue7.set('undefined');
sharedValue8.set('undefined');
sharedValue9.set('undefined');
sharedValue10.set('undefined');
