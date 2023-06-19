$(document).ready(function() {
    $('#githubForm').submit(function(e) {
      e.preventDefault();
      var githubUrl = $('#githubUrl').val();
  
      $.get('/analyze', { githubUrl: githubUrl }, function(data) {
        var resultContainer = $('#resultContainer');
        resultContainer.empty();
  
        if (data.error) {
          resultContainer.append('<p>Error: ' + data.error + '</p>');
        } else {
          resultContainer.append('<p>Repository with the highest technical complexity:</p>');
          resultContainer.append('<a href="' + data.repositoryUrl + '">' + data.repositoryUrl + '</a>');
          resultContainer.append('<p>Complexity Insights:</p>');
          resultContainer.append('<pre>' + data.analysis + '</pre>');
        }
      });
    });
  });
  