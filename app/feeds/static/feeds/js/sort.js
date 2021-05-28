const el = document.getElementById('feedorder');
const sortable = Sortable.create(el, {
  delay: 150,
  delayOnTouchOnly: true,

  onEnd: (evt) => {
    const feeds = document.getElementsByClassName('feed');
    const data = {};
    for (let i = 0, len = feeds.length; i < len; i++) {
      data[feeds[i].id] = i;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    config = {
      headers: {
        'X-CSRFTOKEN': csrftoken,
      },
    };

    // console.debug('Sorted. Making POST request');
    // console.debug(data);
    try {
      const res = axios.post('/feeds/sort', data, config);
    } catch (e) {
      console.error(e);
    }
  },
});
