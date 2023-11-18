var ctx = document.getElementById('averageChart').getContext('2d');
         
        // var avgData = {{ avg_data|safe }}; 
        
        var topics = avgData.map(item => item.topic);
        var avgIntensities = avgData.map(item => item.avg_intensity);
        var avgLikelihoods = avgData.map(item => item.avg_likelihood);
        
        var myChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: topics,
                datasets: [
                    {
                        label: 'Average Intensity',
                        data: avgIntensities,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    },
                    {
                        label: 'Average Likelihood',
                        data: avgLikelihoods,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                    }
                ]
            },
            options: {
                // Customize chart options here
                
            }
        });