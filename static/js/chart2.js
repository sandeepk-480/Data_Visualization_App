var ctx = document.getElementById('sectorChart').getContext('2d');
        
        
        var labels = [];
        var startYears = []; 
        var endYears = [];
        
        sectorYears.forEach(item => {
            labels.push(item.sector);
            
            var startYear = item.years[0].start_year;
            var endYear = item.years[0].end_year;
            
            startYears.push(startYear);
            endYears.push(endYear);
        });
        
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Start Year',
                        data: startYears,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    },
                    {
                        label: 'End Year',
                        data: endYears,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                    }
                ]
            },
            options: {
                scales:{
                    y: {
                        beginAtZero: false,
                        min: 2000,
                        max: 2030,
                        ticks:{
                            stepSize:2
                        }
                    }
                }
                // Customize chart options here
            }
        });