# -*- coding: utf-8 -*-

# Author: Eduardo Vannini
# Date: 27-02-20

import numpy as np
import pandas as pd
import scipy.optimize as opt
import matplotlib.pyplot as plt


class Tests:
    """
    Collection de methodes statiques en rapport avec les tests (creation, visualisation, etc.)
    """
    @staticmethod
    def write_theta(out_path, theta):
        """
        Methode statique qui permet d'ecrire un vecteur d'angles 'theta' (degres) dans un fichier qui soit
        lisible par le programme LabVIEW du projet P4 MAP.

        :param out_path : Chemin du fichier ou le test sera ecrit (ecrase tout fichier de meme nom!).
        :param theta    : Vecteur des angles de commande du servo, en degres.
        :return         : None
        """
        np.savetxt(out_path, theta, fmt="%.7e")
        with open(out_path, "r") as f:
            old = f.read()
        with open(out_path, "w") as f:
            f.write(old.replace(".", ","))

    @staticmethod
    def plot_test(test_path, dt):
        """
        Methode statique qui permet de visualiser le contenu d'un fichier de tests situe au chemin 'test_path'.
        Ce fichier de tests est tel que ceux ecrits par la methode statique 'Tests.write_theta'.

        :param test_path : Chemin vers le fichier de test a visualiser.
        :param dt        : Periode d'echantillonnage utilisee dans ce fichier, en secondes.
        :return          : None
        """
        with open(test_path, "r") as f:
            theta = np.array(list(map(lambda s: float(s.replace(",", ".")), f.read().split())))
        plt.plot(np.arange(0, theta.size * dt, dt), theta)

    @staticmethod
    def write_test_1(out_path, angle_deg, dt, t_max, offset=0):
        """
        Methode statique permettant d'ecrire un test dans lequel l'angle est constant.

        :param out_path  : Chemin vers le fichier de tests a ecrire (ecrase tout fichier de meme nom!).
        :param angle_deg : Valeur de l'angle pour ce test, en degres.
        :param dt        : Periode d'echantillonnage a utiliser dans ce test, en secondes.
        :param t_max     : Duree du test, en secondes.
        :param offset    : offset a ajouter sur l'angle pour eventuellement compenser une imperfection
                           du systeme reel.
        :return          : None
        """
        t = np.arange(0, t_max, dt)
        theta = np.full(t.shape, fill_value=angle_deg)
        theta += offset
        Tests.write_theta(out_path, theta)

    @staticmethod
    def write_test_2(out_path, angle_deg_1, angle_deg_2, dt, t_max, offset=0):
        """
        Methode statique permettant d'ecrire un test dans lequel l'angle evolue lineairement entre
        'angle_deg_1' et 'angle_deg_2' pendant une duree 't_max' [s].

        :param out_path    : Chemin vers le fichier de tests a ecrire (ecrase tout fichier de meme nom!).
        :param angle_deg_1 : Valeur de l'angle initial, en degres.
        :param angle_deg_2 : Valeur de l'angle final, en degres.
        :param dt          : Periode d'echantillonnage a utiliser dans ce test, en secondes.
        :param t_max       : Duree du test, en secondes.
        :param offset      : offset a ajouter sur l'angle pour eventuellement compenser une imperfection
                             du systeme reel.
        :return            : None
        """
        theta = np.linspace(angle_deg_1, angle_deg_2, int(t_max / dt))
        theta += offset
        Tests.write_theta(out_path, theta)

    @staticmethod
    def write_test_3(out_path, a, p, dt, t_max, offset=0):
        """
        Methode statique permettant d'ecrire un test dans lequel l'angle suit un sinus de periode
        'p' [s] et d'amplitude 'a' [deg] pendant un duree 't_max' [s].

        :param out_path : Chemin vers le fichier de tests a ecrire (ecrase tout fichier de meme nom!).
        :param a        : Amplitude du sinus, en degres.
        :param p        : Periode du sinus, en secondes.
        :param dt       : Periode d'echantillonnage a utiliser dans ce test, en secondes.
        :param t_max    : Duree du test, en secondes.
        :param offset   : offset a ajouter sur l'angle pour eventuellement compenser une imperfection
                          du systeme reel.
        :return         : None
        """
        t = np.arange(0, t_max, dt)
        theta = a * np.sin(2 * np.pi / p * t)
        theta += offset
        Tests.write_theta(out_path, theta)

    @staticmethod
    def write_test_4(out_path, a1, a2, t1, t2, dt, t_max, offset=0):
        """
        Methode statique permettant d'ecrire un test constitue de trois etapes:
            1) L'angle est maintenu a une valeur de 'a1' [deg] pendant 't1' [s];
            2) L'angle est maintenu a une valeur de 'a2' [deg] pendant 't2' [s];
            3) L'angle est mis a 0 deg pendant le temps restant.
        But du test: mettre la balle d'un cote du tube, puislui donner de la vitesse,
                     pour finalement la laisser rouler d'elle-meme.

        :param out_path : Chemin vers le fichier de tests a ecrire (ecrase tout fichier de meme nom!).
        :param a1       : Amplitude de l'angle pour l'etape 1) [deg].
        :param a2       : Amplitude de l'angle pour l'etape 2) [deg].
        :param t1       : Duree de l'etape 1) [s].
        :param t2       : Duree de l'etape 2) [s].
        :param dt       : Periode d'echantillonnage a utiliser dans ce test, en secondes.
        :param t_max    : Duree du test, en secondes.
        :param offset   : offset a ajouter sur l'angle pour eventuellement compenser une imperfection
                          du systeme reel.
        :return         : None
        """
        t = np.arange(0, t_max, dt)
        theta = np.zeros(t.shape)
        theta[:int(t1 / dt)] = a1
        theta[int(t1 / dt):int(t1 / dt) + int(t2 / dt)] = a2
        theta[int(t1 / dt) + int(t2 / dt):] = 0
        theta += offset
        Tests.write_theta(out_path, theta)

    @staticmethod
    def write_test_5(out_path, p, dt, t_max, offset=0):
        """
        Methode statique permettant d'ecrire un test ou l'angle suit une loi "sin * exp(t / 7)"
        dans laquelle le sinus a une periode de 'p' [s].

        :param out_path : Chemin vers le fichier de tests a ecrire (ecrase tout fichier de meme nom!).
        :param p        : Periode de la composante sinusoidale du test [s].
        :param dt       : Periode d'echantillonnage a utiliser dans ce test, en secondes.
        :param t_max    : Duree du test, en secondes.
        :param offset   : offset a ajouter sur l'angle pour eventuellement compenser une imperfection
                          du systeme reel.
        :return         : None
        """
        t = np.arange(0, t_max, dt)
        theta = np.sin(t * 2 * np.pi / p) * np.exp(t / 7)
        theta += offset
        Tests.write_theta(out_path, theta)

    @staticmethod
    def update_decimal_sep(data_path):
        """
        Methode statique qui permet de remplacer tous les "," d'un fichier par des ".". Permet de rendre les
        fichiers d'observations experimentales de LabVIEW plus utilisables.

        Attention: *toutes* les virgules seront remplacees. On fait donc l'hypothese que les seules virgules
                   du fichier sont celles pour les separateurs decimaux.

        :param data_path : Chemin vers le fichier a modifier.
        :return          : None
        """
        with open(data_path, "r") as f:
            old = f.read()
        with open(data_path, "w") as f:
            f.write(old.replace(",", "."))

    @staticmethod
    def update_decimal_sep_dir(dir_path):
        """
        Methode statique qui permet d'appliquer la correstion des separateurs decimaux faite par 'update_decimal_sep'
        a tous les fichiers d'un repertoire.

        Note: Si d'autres fichiers que des fichiers de donnees LabVIEWse trouvent dans le reperoire, ils seront
              aussi modifies (leurs "," deviendront des ".").

        :param dir_path : Chemin vers le repertoire contenant les fichiers a modifier.
        :return         : None
        """
        for filename in os.listdir(dir_path):
            Tests.update_decimal_sep(os.path.join(dir_path, filename))

    @staticmethod
    def plot_bb_test_output(data_path, dt, title=None, pos_lims=(-0.775 / 2, 0.775 / 2), theta_lims=(-50, 50)):
        """
        Methode statique qui permet de faire un graphe pour representer des donnees experimentales du
        Ball and Beam du P4 MAP. Les donnees experimentales sont contenues dans le fichier dont le chemin
        est 'data_path' et sont formatees de la meme maniere que ce que genere LabVIEW.

        Note: Le fichier situe en 'data_path' doit avoir ete traite avec 'update_decimal_dep' pour
              etre utilisable.

        :param data_path  : Chemin vers le fichier contenant les donnees experimentales.
        :param dt         : Periode d'echantillonnage utilisee dans le fichier d'observations experimentales.
        :param title      : Titre de la figure. Sera remplace par le nom du fichier si il n'est pas specifie.
        :param pos_lims   : Tuple contenant les valeurs limites a afficher sur le graphe des positions (permet
                            de dimensionner le graphe). Si 'pos_lims' vaut None, les limites sont automatiques.
        :param theta_lims : Tuple contenant les valeurs limites a afficher sur le graphe des angles (permet
                            de dimensionner le graphe). Si 'theta_lims' vaut None, les limites sont automatiques.
        :return           : Un tuple (fig, ax_pos, _ax_theta) avec:
                                - fig      : La figure contenant les deux plots;
                                - ax_pos   : Le plot contenant les positions;
                                - ax_theta : Le plot contenant les angles.
        """
        df = pd.read_csv(data_path, sep="\t", index_col=0, skiprows=2, header=0, usecols=[0, 1, 2],
                         names=["timestep", "theta_deg", "pos_cm"])
        fig, ((ax_pos), (ax_theta)) = plt.subplots(2, sharex=True)
        ax_pos.plot(df.index * dt, df.pos_cm / 100, label="Measured position [m]")
        ax_theta.plot(df.index * dt, df.theta_deg, label="Commanded angle (servo) [deg]")
        ax_pos.legend()
        ax_theta.legend()
        ax_pos.grid()
        ax_theta.grid()
        if pos_lims:
            ax_pos.set_ylim(pos_lims)
        if theta_lims:
            ax_theta.set_ylim(theta_lims)
        ax_pos.set_xlabel("Time [s]")
        ax_theta.set_xlabel("Time [s]")
        ax_pos.set_ylabel("Position [m]")
        ax_theta.set_ylabel("Angle [deg]")
        fig.suptitle(data_path if title is None else title)
        return fig, ax_pos, ax_theta

    @staticmethod
    def plot_bb_test_output_and_sim(data_path, bbsimulator, title=None, command_noise_func=lambda *args, **kwargs: 0,
                                    output_noise_func=lambda *args, **kwargs: 0):
        """
        Methode statique qui permet de faire un graphe pour representer des donnees experimentales du
        Ball and Beam du P4 MAP en les comparant aux donnees simulees pour les memes conditions.
        Les donnees experimentales sont contenues dans le fichier dont le chemin est 'data_path' et sont
        formatees de la meme maniere que ce que genere LabVIEW. Le simulateur doit etre de type

        Note: Le fichier situe en 'data_path' doit avoir ete traite avec 'update_decimal_dep' pour
              etre utilisable.

        :param data_path          : Chemin vers le fichier contenant les donnees experimentales.
        :param bbsimulator        : Objet de type 'BBSimualtor' representant la simulation du Ball and Beam.
        :param title              : Titre de la figure. Sera remplace par le nom du fichier si il n'est pas specifie.
        :param command_noise_func : Fonction retournant le bruit a ajouter a la commande au temps 'timestep'. Signature:
                                    command_noise_func(timestep, params, all_t, all_u, all_y, dt)
        :param output_noise_func  : Fonction retournant le bruit a ajouter a la sortie au temps 'timestep'. Signature:
                                    output_noise_func(timestep, params, all_t, all_u, all_y, dt)
        :return                   : Un tuple (fig, ax_pos, _ax_theta) avec:
                                        - fig      : La figure contenant les deux plots;
                                        - ax_pos   : Le plot contenant les positions;
                                        - ax_theta : Le plot contenant les angles.
        """
        dt, l = bbsimulator.dt, bbsimulator.params["l"]
        df = pd.read_csv(data_path, sep="\t", index_col=0, skiprows=2, header=0, usecols=[0, 1, 2],
                         names=["timestep", "theta_deg", "pos_cm"])
        init_state = np.zeros((2,))
        init_state[0] = df.pos_cm[0] / 100
        init_state[1] = (df.pos_cm[1] - df.pos_cm[0]) / dt / 100
        bbsimulator.simulate(lambda timestep, *args, **kwargs: np.deg2rad(df.theta_deg[timestep]),
                             command_noise_func, output_noise_func, n_steps=df.shape[0], init_state=init_state)
        fig, ((ax_pos), (ax_theta)) = plt.subplots(2, sharex=True)
        ax_pos.plot(df.index * dt, df.pos_cm / 100, label="Measured position [m]")
        ax_pos.plot(bbsimulator.all_t[:df.shape[0]], bbsimulator.all_y[:df.shape[0]], label="Simulated position [m]")
        ax_theta.plot(df.index * dt, df.theta_deg, label="Commanded angle (servo) [deg]")
        ax_theta.plot(bbsimulator.all_t[:df.shape[0]], np.rad2deg(bbsimulator.all_u[:df.shape[0]]),
                      label="Actual offset angle (servo) [deg]")
        ax_pos.legend()
        ax_theta.legend()
        ax_pos.grid()
        ax_theta.grid()
        ax_pos.set_ylim((-l / 2 - 0.05, l / 2 + 0.05))
        ax_theta.set_ylim((-50 - 5, 50 + 5))
        ax_pos.set_xlabel("Time [s]")
        ax_theta.set_xlabel("Time [s]")
        ax_pos.set_ylabel("Position [m]")
        ax_theta.set_ylabel("Angle [deg]")
        fig.suptitle(data_path if title is None else title, fontsize=14)
        return fig, ax_pos, ax_theta

    @staticmethod
    def fit_bb_sim_params(training_data_paths, param_names, bbsimulator, method="SLSQP", bounds=None,
                          command_noise_func=lambda *args, **kwargs: 0, output_noise_func=lambda *args, **kwargs: 0):
        """
        Methode statique permettant d'optimiser les parametres 'param_names' du simulateur 'bbsimulator' afin
        de minimiser la somme des erreurs quadratiques moyennes (MSE) sur l'ensemble des fichiers de donnees
        experimentales dont les chemins sont contenus dans 'training_data_paths'.

        Des bornes peuvent etre appliquees sur les valeurs des parametres. Elles sont a fournir sous forme
        d'une liste de tuples (min, max), dans le meme ordre que les parametres donnes dans 'param_names'.
        La methode d'optimisation peut ete choisie. Voir la documentation de la fonction scipy.optimize.minimize
        (attention, certaines methodes ne sont pas compatibles avec l'utilisation de bornes).

        Du bruit peut etre pris en compte dans la simulation avec les arguments 'command_noise_func' et
        'output_noise_func', mais par defaut il n'y en a pas.

        Note importante: les parametres de l'objet 'bbsimulator' sont modifies durant le processus, mais rien
                         ne garantit qu'ils soient optimals a la fin. Les parametres optimaux sont a lire
                         dans l'objet 'OptimizationResult' retourne par la fonction et sont a appliquer
                         a la main si la MSE semble satisfaisante.

        :param training_data_paths : Liste des chemins vers les fichiers de donnees experimentales LabVIEW.
                                     Les separateurs decimaux doivent etre remplaes par des ".".
        :param param_names         : Liste des noms des parametres sur lesquels l'optimisation peut s'effectuer.
                                     Ces noms correspondent aux cles du dictionnaire 'params' de 'bbsimulator'.
        :param bbsimulator         : Objet de type 'BBSimulator' representant la modelisation du systeme et que
                                     l'on desire optimiser.
        :param bounds              : Liste de tuples (min, max) correspondant aux bornes imposees sur les
                                     parametres contenus dans 'param_names'. None represente une borne non
                                     specifiee.
        :param command_noise_func  : Fonction de bruit sur la commande telle qu'acceptee par la methode
                                     'bbsimulator.simulate'.
        :param output_noise_func   : Fonction de bruit sur la mesure telle qu'acceptee par la methode
                                     'bbsimulator.simulate'.
        :return                    : Objet 'OptimizationResult' contenant le resultat de l'optimisation.
        """
        def err_func(param_values):
            """
            Fonction retournant la somme des MSE sur l'ensemble des fichiers de test. On desire minimiser
            cette fonction. Elle est faite pour etre utilisee dans la fonction 'scipy.optimize.minimize'.

            :param param_values : Valeurs des parametres a utiliser, dans le meme ordre que 'param_names'.
            :return             : La MSE totale.
            """
            # Set les parametres
            for param_name, param_value in zip(param_names, param_values):
                bbsimulator.params[param_name] = param_value

            tot_mse = 0
            for data_path in training_data_paths:
                df = pd.read_csv(data_path, sep="\t", index_col=0, skiprows=2, header=0, usecols=[0, 1, 2],
                                 names=["timestep", "theta_deg", "pos_cm"])
                init_state = np.zeros((2,))
                init_state[0] = df.pos_cm[0] / 100
                init_state[1] = (df.pos_cm[1] - df.pos_cm[0]) / bbsimulator.dt / 100
                bbsimulator.simulate(lambda timestep, *args, **kwargs: np.deg2rad(df.theta_deg[timestep]),
                                     command_noise_func, output_noise_func, n_steps=df.shape[0], init_state=init_state)
                partial_mse = np.sum(np.power(np.abs(bbsimulator.all_y[:df.shape[0]].flatten() - df.pos_cm / 100), 2))
                tot_mse += partial_mse

            print("Parameters: {};    mean MSE per file: {}".format(np.round(param_values, 5),
                                                                    tot_mse / len(training_data_paths)))
            return tot_mse

        init_params = np.array([bbsimulator.params[param_name] for param_name in param_names])

        # Methodes possibles avec 'bounds': "TNC", "L-BFGS-B", "SLSQP".
        return opt.minimize(err_func, init_params, method=method, bounds=bounds)


if __name__ == "__main__":
    from BBSimulators import BBThetaSimulator
    import os

    # Creation du simulateur que l'on veut optimiser
    DT = 0.05
    sim = BBThetaSimulator()

    # Ici, on peut modifier certains parametres du simulateur. C'est pratique quand
    # on veut appliquer des parametres issus d'une minimisation de l'erreur sans
    # forcement changer les valeurs par defaut dans les classes.
    sim.params["theta_offset"] = -1.07698393e-01
    sim.params["kf"] = 1.63537967e+01
    sim.params["m"] = 1.39728756e-01
    sim.params["jb"] = 8.29530009e-04
    sim.params["ff_pow"] = 2.23113062e+00

    # Dossier de base contenant tous les fichiers de donnees experimentales
    # (et rien d'autre, sinon probleme avec la fonction 'Tests.update_decimal_sep_dir').
    expdata_dir = "./Tests Output/Data_Exp"

    # Mettre a jour la representation des separateurs decimaux pour tous les fichiers
    # de donnees. Le changement sera applique a *tous* les fichiers contenus dans 'expdata_dir'.
    # (a ne faire qu'une fois).
    # Tests.update_decimal_sep_dir(expdata_dir)

    # Ensemble des fichiers de donnees. A decommenter un a un pour verifier que les parametres
    # qu'on a mis dans le simulateur donnent des bons resultats.
    # datafile = "test_1_0_out.txt"
    # datafile = "test_1_20_out.txt"
    # datafile = "test_1_-40_out.txt"
    # datafile = "test_2_0_20_out.txt"
    # datafile = "test_2_40_0_out.txt"
    # datafile = "test_3_10_5_out.txt"
    # datafile = "test_3_20_5_out_edited.txt"
    # datafile = "test_3_20_10_out_edited.txt"
    # datafile = "test_3_30_5_out.txt"
    # datafile = "test_3_40_5_out.txt"
    # datafile = "test_4_-30_30_10_2_out.txt"
    # datafile = "test_4_-30_30_10_2_out_nul.txt"  # Ignorer ce test: trop bizarre
    # datafile = "test_4_-30_30_10_5_out.txt"
    # datafile = "test_4_-30_30_10_5_out_nul.txt"  # Ignorer ce test: trop bizarre
    # datafile = "test_4_-40_40_10_2_out.txt"
    # datafile = "test_4_-40_40_10_2_out_nul.txt"  # Ignorer ce test: trop bizarre
    # datafile = "test_4_-40_40_10_5_out.txt"
    # datafile = "test_4_-40_40_10_5_out_nul.txt"  # Ignorer ce test: trop bizarre
    # datafile = "test_sinexp_1_out.txt"
    datafile = "test_sinexp_5_out.txt"

    # Affichage d'un graphe qui compare les vrais resultats experimentaux et les resultats de la
    # simulation pour le fichier 'datafile' choisi.
    data_path = os.path.join(expdata_dir, datafile)
    Tests.plot_bb_test_output_and_sim(data_path, sim, "Comparaison experience vs. simulation")
    plt.show()

    if input("'y' pour lancer l'optimisation, autre touche pour terminer: ").lower() != "y":
        exit(0)

    # Selection des fichiers de donnees experimentales que l'on s'autorise a utiliser pour optimiser
    # le simulateur. Il ne faut pas en choisir de trop, sinon on risque l'overfitting (c'est-a-dire que
    # le simulateur va "apprendre par coeur" les resultats experimentaux pour ces fichiers-la, mais ne
    # sera pas capable d'extrapoler pour des situations un peu differentes, ce qui n'est pas ideal).
    training_data_files = [
        "test_1_20_out.txt",
        "test_2_0_20_out.txt",
        "test_3_10_5_out.txt",
        "test_3_20_5_out_edited.txt",
        "test_4_-30_30_10_2_out.txt",
        "test_sinexp_5_out.txt"
    ]

    # Noms des parametres sur lesquels on veut effectuer l'optimisation. Ces noms correspondent
    # aux cles du dictionnaire 'params' du simulateur.
    param_names = ["theta_offset", "kf", "m", "jb", "ff_pow"]

    # Dans le meme ordre que pour 'param_names', donner les bornes sur les valeurs des parametres.
    # Pour une borne non-specifiee, utiliser None.
    bounds = [(np.deg2rad(-20), np.deg2rad(20)), (0, None), (20 / 1000, 200 / 1000), (1e-06, 1e-02), (0, 5)]

    # Utiliser un iterable normal et pas un generateur pour les 'training_paths', sinon probleme.
    training_data_paths = tuple(map(lambda file: os.path.join(expdata_dir, file), training_data_files))

    # Lancement de l'optimisation (peut prendre un peu de temps).
    res = Tests.fit_bb_sim_params(training_data_paths, param_names, sim, bounds=bounds)

    # Affichage de l'OptimizeResult retourne. Les valeurs optimales et la MSE correspondantes se trouvent
    # ici. On retrouve aussi un status indiquant si l'optimisation a echoue ou non. Pour tester ces valeurs
    # il faut les remplacer a la main a l'endroit ci-dessus prevu a cet effet.
    print(res)
