module privateer {
  import trading;
  import random_encounters;
  import garbage_collect;
  import difficulty;
  bool garbage;
  void init (float sigdis, float detectiondis, float gendis, int minships, int genships, float fighterprob, float enemyprob, float capprob, float credits_to_maximize_difficulty, float enemy_credits_begin, float enemy_credits_earned,float garbage_collect_dist, float capdist) {//negative garbage collect dist disables that feature
    difficulty.init (credits_to_maximize_difficulty,enemy_credits_begin, enemy_credits_earned);
    random_encounters.init (sigdis, detectiondis, gendis, minships,genships,fighterprob,capprob,enemyprob,capdist);
    garbage=false;
    if (garbage_collect_dist>0.0) {
      garbage_collect.init (garbage_collect_dist);
      garbage=true;
    }
    trading.init();
  };
  void loop() {
    difficulty.loop();
    trading.loop();
    random_encounters.loop();
    if (garbage) {
      garbage_collect.loop();
    }
  };
  void initstarsystem() {
    random_encounters.initstarsystem();
  };
}
