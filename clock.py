from time import time
from twautomate import seed_db
from twautomate import get_new_followers
from twautomate import get_old_followers
from twautomate import send_direct_message
from twautomate import save_followers
from config import tw_username
from config import scheduler_time
from apscheduler.schedulers.blocking import BlockingScheduler


if __name__ == "__main__":
    def tasks():
        t1 = time()
        old = get_old_followers(tw_username)
        new = get_new_followers(tw_username)
        new_followers = list(set(new).difference(set(old)))

        save_followers(tw_username, new)

        for n in new_followers:
            print("Mensagem enviada para {}".format(n))
            send_direct_message(n)
        print("Tarefa Completa")
        t2 = time()
        print("Tarefa concluída em segundo: ", t2-t1)

    seed_db(tw_username)
    tasks()
    sched = BlockingScheduler()
    @sched.scheduled_job('intervalo', minutes=scheduler_time)
    def timed_job():
        try:
            tasks()
        except Exception as error:
            print("Erro do agendador: ", error)


    sched.start()
