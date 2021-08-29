$.ajax({
  type:"POST",
  url: '/suggestions',
  data:{},
  success: function(data){
    var clist={},flist={};
    data.clist.forEach(element => {
      clist[element]=null;
    });
    $('input.autocomplete#autocomplete-input1').autocomplete({
      data: clist,
    });
    data.flist.forEach(element => {
      flist[element]=null;
    });
    $('input.autocomplete#autocomplete-input2').autocomplete({
      data: flist,
    });

  }
});