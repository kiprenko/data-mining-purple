# data-mining-purple
This repository stores my simple data-mining scripts.
These tasks were implemented in the scope of my university study at the 4th course.
The repository contains only Python scripts.
You may need additional (very popular and easy to install) Python libraries. Such as:

* matplotlib
* networkx
* numpy
* nltk
* pandas

I won't list all of them here, because I'm sure you will figure out what libraries you require and how to install them on your own.<br>
The "purple" word was added to the repository name just to differ the repository from my other possible data-mining repositories.

## Description
The repository consist of five parts:

1. data-statistical-analysis
2. naive-bayes-classifier
3. k-means-method
4. page-rank
5. market-basket-analysis

All these parts have their own folder where you find everything you need to run the scripts.

### page-rank
The script builds a page graph of the site and calculates the site's pages rank.
You can run the script by the next command:<br>

`python main.py http://thedemosite.co.uk/`

For our example, you will see the next graph

![page-rank-graph-example](docs/page-rank/page-rank-graph.png)

The page rank of the pages you will find in the console (terminal) output:<br>

```
{
    "/": 0.018750000000000003,
    "index.php": 0.17862779158724276,
    "thedatabase.php": 0.17862779158724276,
    "addauser.php": 0.17862779158724276,
    "login.php": 0.17862779158724276,
    "getyourowndbonline.php": 0.17862779158724273,
    "addausercode.php": 0.044055521031893,
    "logincode.php": 0.044055521031893
}
```

## Author :panda_face:

- Name: Evgeniy Kiprenko
- Email: zhenyakiprenko@gmail.com
- [LinkedIn](https://www.linkedin.com/in/evgeniy-kiprenko/)
- [Telegram](https://t.me/Jus7XV)
