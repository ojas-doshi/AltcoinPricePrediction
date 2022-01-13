package net.smallacademy.otpauth;

import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.drawerlayout.widget.DrawerLayout;

import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.material.navigation.NavigationView;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;

public class MainActivity extends AppCompatActivity {
    public static final String TAG = "TAG";
    FirebaseAuth firebaseAuth;
    FirebaseFirestore fStore;
    TextView fullName,email,phone;
    String mName,mEmail,mPhone;
    Toolbar toolbar;
    DrawerLayout drawerLayout;
    NavigationView navigationView;
    Menu menu;
    TextView textView;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        /*---------------------Hooks------------------------*/
//        drawerLayout=findViewById(R.id.drawer_layout);
//        navigationView=findViewById(R.id.nav_view);
//        textView=findViewById(R.id.textView);
//        toolbar=findViewById(R.id.toolbar);
//
//
//
//        setSupportActionBar(toolbar);
//
//
//        ActionBarDrawerToggle toggle=new ActionBarDrawerToggle(this, drawerLayout, toolbar,R.string.navigation_drawer_open,R.string.navigation_drawer_close);
//        drawerLayout.addDrawerListener(toggle);
//        toggle.syncState();




        toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setTitle("Profile");
        firebaseAuth = FirebaseAuth.getInstance();
        fStore = FirebaseFirestore.getInstance();

        fullName = findViewById(R.id.profileFullName);
        email = findViewById(R.id.profileEmail);
        phone = findViewById(R.id.profilePhone);

        DocumentReference docRef =fStore.collection("users").document(firebaseAuth.getCurrentUser().getUid());
        docRef.get().addOnSuccessListener(new OnSuccessListener<DocumentSnapshot>() {
            @Override
            public void onSuccess(DocumentSnapshot documentSnapshot) {
                if(documentSnapshot.exists()){
                    mName = documentSnapshot.getString("first") + " " + documentSnapshot.getString("last");
                    mEmail = documentSnapshot.getString("email");
                    mPhone = firebaseAuth.getCurrentUser().getPhoneNumber();

                    fullName.setText(mName);
                    email.setText(mEmail);
                    phone.setText(mPhone);
                }else {
                    Log.d(TAG, "Retrieving Data: Profile Data Not Found ");
                }
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main_menu,menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id=item.getItemId();
        if(id == R.id.nav_logout){
            FirebaseAuth.getInstance().signOut();
            startActivity(new Intent(getApplicationContext(),Register.class));
            finish();
        }
        else if (id==R.id.nav_home){
            Intent intent=new Intent(MainActivity.this, present.class);
            startActivity(intent);
        }
        else if (id==R.id.nav_profile){
            Intent intent=new Intent(MainActivity.this, MainActivity.class);
            startActivity(intent);

        }else if (id==R.id.nav_trend){
            Intent intent=new Intent(MainActivity.this, present.class);
            startActivity(intent);

        }
        return true;
    }
}
