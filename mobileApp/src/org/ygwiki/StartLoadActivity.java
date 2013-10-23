package org.ygwiki;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ComponentName;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.content.Intent;
import android.os.Handler;
import android.preference.PreferenceManager;
import android.view.WindowManager;
import android.widget.Toast;


public class StartLoadActivity extends Activity {

    //time for picture display
    private static final int LOAD_DISPLAY_TIME = 2500;

    // 获取默认的SharedPreferences
    private SharedPreferences sharedPreferences ;

    // 从SharedPreferences获取是否存在快捷方式 若不存在返回false 程序第一次进来肯定返回false
    boolean isExist ;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

//        getWindow().setFormat(PixelFormat.RGBA_8888);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setContentView(R.layout.load);

        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);
        boolean firstTime = prefs.getBoolean("first_time", true);
        if (firstTime){    // if is first time start app, tip whether need to install shortcut

            //show the tip dialog
            (new  AlertDialog.Builder(this))
                    .setTitle(R.string.welcome_title)
                    .setMessage(R.string.tip_create_shortcut)
                    .setPositiveButton(R.string.confirm_yes,new ConfirmCreateShortcutListener(this))
                    .setNegativeButton(R.string.confirm_no, new CancleCreateShortcutListener(this))
                    .show();


            SharedPreferences.Editor pEdit = prefs.edit();
            pEdit.putBoolean("first_time", false);
            pEdit.commit();

        } else {

            (new Handler()).postDelayed(new DeplayThread(this), LOAD_DISPLAY_TIME);

        }

    }

    //Deplay thread
    private class DeplayThread implements Runnable {

        private StartLoadActivity activity;

        public  DeplayThread(StartLoadActivity activity){

            this.activity = activity;
        }

        @Override
        public void run() {

            //Go to main activity, and finish load activity
            Intent mainIntent = new Intent(StartLoadActivity.this, WikipediaActivity.class);
            StartLoadActivity.this.startActivity(mainIntent);
            StartLoadActivity.this.finish();
        }
    }


    //comfirm create shortcut listener
    private class ConfirmCreateShortcutListener implements   DialogInterface.OnClickListener{

        private StartLoadActivity activity;

        public  ConfirmCreateShortcutListener(StartLoadActivity activity){

            this.activity = activity;
        }


        @Override
        public void onClick(DialogInterface dialogInterface, int i) {

            this.addShortcut();//create short cut
            (new Handler()).postDelayed(new DeplayThread(this.activity), LOAD_DISPLAY_TIME);
        }

        /**
         * 为程序创建桌面快捷方式
         */
        private void addShortcut(){
            Intent shortcut = new Intent("com.android.launcher.action.INSTALL_SHORTCUT");

            //快捷方式的名称
            shortcut.putExtra(Intent.EXTRA_SHORTCUT_NAME, getString(R.string.app_name));
            shortcut.putExtra("duplicate", false); //不允许重复创建

            ComponentName comp = new ComponentName(getPackageName(), "."+getLocalClassName());
            shortcut.putExtra(Intent.EXTRA_SHORTCUT_INTENT, new Intent(Intent.ACTION_MAIN).setComponent(comp));

            //快捷方式的图标
            Intent.ShortcutIconResource iconRes = Intent.ShortcutIconResource.fromContext(this.activity, R.drawable.icon);
            shortcut.putExtra(Intent.EXTRA_SHORTCUT_ICON_RESOURCE, iconRes);

            sendBroadcast(shortcut);
            Toast.makeText(this.activity, R.string.shortcut_create_success, Toast.LENGTH_LONG).show();
        }
    }


    //cancel create shortcut listener
    private class CancleCreateShortcutListener implements   DialogInterface.OnClickListener{

        private StartLoadActivity activity;

        public  CancleCreateShortcutListener(StartLoadActivity activity){

            this.activity = activity;
        }


        @Override
        public void onClick(DialogInterface dialogInterface, int i) {

            (new Handler()).postDelayed(new DeplayThread(this.activity), LOAD_DISPLAY_TIME);
        }


    }



}