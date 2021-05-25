
function slist(target) {
  // (A) GET LIST + ATTACH CSS CLASS
  target = document.getElementById(target);
  target.classList.add('slist');

  // (B) MAKE ITEMS DRAGGABLE + SORTABLE
  const items = target.getElementsByTagName('li');
  let current = null;
  for (const i of items) {
    // (B1) ATTACH DRAGGABLE
    i.draggable = true;

    // (B2) DRAG START - YELLOW HIGHLIGHT DROPZONES
    i.addEventListener('dragstart', function(ev) {
      current = this;
      for (const it of items) {
        if (it != current) {
          it.classList.add('hint');
        }
      }
    });

    // (B3) DRAG ENTER - RED HIGHLIGHT DROPZONE
    i.addEventListener('dragenter', function(ev) {
      if (this != current) {
        this.classList.add('active');
      }
    });

    // (B4) DRAG LEAVE - REMOVE RED HIGHLIGHT
    i.addEventListener('dragleave', function() {
      this.classList.remove('active');
    });

    // (B5) DRAG END - REMOVE ALL HIGHLIGHTS
    i.addEventListener('dragend', function() {
      for (const it of items) {
        it.classList.remove('hint');
        it.classList.remove('active');
      }
    });

    // (B6) DRAG OVER - PREVENT THE DEFAULT "DROP", SO WE CAN DO OUR OWN
    i.addEventListener('dragover', function(evt) {
      evt.preventDefault();
    });

    // (B7) ON DROP - DO SOMETHING
    i.addEventListener('drop', function(evt) {
      evt.preventDefault();
      if (this != current) {
        let currentpos = 0; let droppedpos = 0;
        for (let it=0; it<items.length; it++) {
          if (current == items[it]) {
            currentpos = it;
          }
          if (this == items[it]) {
            droppedpos = it;
          }
        }
        if (currentpos < droppedpos) {
          this.parentNode.insertBefore(current, this.nextSibling);
        } else {
          this.parentNode.insertBefore(current, this);
        }
      }

			var data = {};
      for (let i = 0, len = items.length; i < len; i++) {
				data[items[i]['id']] = i;
      }
			console.log('Sorted');

			const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

			config = {
				headers : {
					'X-CSRFTOKEN': csrftoken
				}
			}

			console.log("Making POST request");
			try {
				const res = axios.post('/feeds/sort', data, config);
			} catch (e) {
				console.error(e);
			}
    });
  }
}
