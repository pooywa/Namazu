from app.collectors import main as col_main
from app.database import main as db_main
from app.analytics import main as alyt_main
from app.visualization import main as vis_main
from app.utils.reseting import main as res_main
from app.query import main as q_main

if __name__ == "__main__":

    menuitem = ["start","exit"]

    is_runing = True

    while is_runing:


        for i,menu in enumerate(menuitem):
            print(f"{i+1}) {menu}")

        try:
            user_choise = menuitem[int(input("chose a number: "))-1] 

        except ValueError as e:
            print(f"please enter just a number example (1-{len(menuitem)})")
            continue

        except IndexError as e:
            print(f"please chose 1-{len(menuitem)}")
            continue


        match user_choise:
            case "start":
                res_main()
                col_main()
                db_main()
                alyt_main()
                vis_main()
                q_main()

            case "exit":
                print("koja miri lovley mentor taze berenj khis kardam :)")
                is_runing = False



