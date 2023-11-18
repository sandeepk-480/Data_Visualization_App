var topic_ctx = document.getElementById('mychart').getContext('2d');
var topicData = topics_json;
// console.log(topicData,'----');

var topic_chart = new Chart(topic_ctx, {
  type: 'polarArea',
  data: {
    labels: Object.keys(topicData),
    datasets: [
      {
        label: 'topics',
        data: Object.values(topicData),
      }
    ],
  }
});